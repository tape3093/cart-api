import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import Rule
from ..serializers import RuleSerializer


client = APIClient()

class CartRuleListTest(APITestCase):
    def setUp(self):
        Rule.objects.create(
            rule_type='OL', order_limit=100)
        Rule.objects.create(
            rule_type='PD', product_count=5)
        Rule.objects.create(
            rule_type='OD', order_value=20, discount_on_value=1)
        Rule.objects.create(
            rule_type='OD', order_value=50, discount_on_value=2)

    def test_get_all_rules(self):
        response = self.client.get('/api/cart/rules')
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CartRuleCreateTest(APITestCase):
    def setUp(self):
        Rule.objects.create(
            rule_type='OL', order_limit=100)
        self.new_pd_rule = {
            'rule_type': 'PD',
            'product_count': 5
        }
        self.bad_request = {
            'rule_type': 'OM',
            'order-limit': 'test',
            'product_count': 5
        }
        self.new_ol_rule = {
            'rule_type': 'OL',
            'order_limit': 10
        }

    def test_post_new_rule(self):
        response = self.client.post('/api/cart/rule',
                                    data=json.dumps(self.new_pd_rule),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_bad_request(self):
        response = self.client.post('/api/cart/rule',
                                    data=json.dumps(self.bad_request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_dublicate_order_limit_rule(self):
        response = self.client.post('/api/cart/rule',
                                    data=json.dumps(self.new_ol_rule),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class CartRuleChangeTest(APITestCase):
    def setUp(self):
        self.ol_rule = Rule.objects.create(
            rule_type='OL', order_limit=100)
        self.pd_rule = Rule.objects.create(
            rule_type='PD', product_count=5)
        self.od_rule1 = Rule.objects.create(
            rule_type='OD', order_value=20, discount_on_value=1)
        self.od_rule2 = Rule.objects.create(
            rule_type='OD', order_value=50, discount_on_value=2)
        self.new_ol_rule = {
            'rule_type': 'OL',
            'order_limit': 50
        }
        self.bad_request = {
            'rule_type': 'PD',
            'product_count': 'string instead of integer'
        }

    def test_update_existing_rule(self):
        response = self.client.put('/api/cart/rule/' + str(self.ol_rule.pk),
                                    data=json.dumps(self.new_ol_rule),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_non_existing_rule(self):
        response = self.client.put('/api/cart/rule/30',
                                    data=json.dumps(self.new_ol_rule),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_non_existing_rule(self):
        response = self.client.put('/api/cart/rule/' + str(self.pd_rule.pk),
                                    data=json.dumps(self.bad_request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_rule(self):
        response = self.client.delete('/api/cart/rule/' + str(self.ol_rule.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existing_rule(self):
        response = self.client.delete('/api/cart/rule/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)