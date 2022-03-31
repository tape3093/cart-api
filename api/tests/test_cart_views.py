import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import Cart, Product, Rule
from ..serializers import CartSerializer


client = APIClient()

class CartListTest(APITestCase):
    def setUp(self):
        self.cola = Product.objects.create(
            name='Coca Cola', description='Most popular drink', price=1.20)
        self.sprite = Product.objects.create(
            name='Sprite', description='Tastes like lemon', price=1.25)
        self.fanta = Product.objects.create(
            name='Fanta', description='Nobody likes it but its still on the market', price=0.99)
        self.kvass = Product.objects.create(
            name='Kvass', description='Just like beer but its not', price=3.00)
        Cart.objects.create(
            product_id=self.cola, quantity=2)
        Cart.objects.create(
            product_id=self.sprite, quantity=3)
        Cart.objects.create(
            product_id=self.fanta, quantity=10)
        Cart.objects.create(
            product_id=self.kvass, quantity=5)

    def test_get_all(self):
        response = self.client.get('/api/cart/')
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_all(self):
        response = self.client.delete('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CartAddTest(APITestCase):
    def setUp(self):
        self.cola = Product.objects.create(
            name='Coca Cola', description='Most popular drink', price=1.20)
        self.sprite = Product.objects.create(
            name='Sprite', description='Tastes like lemon', price=1.25)
        self.fanta = Product.objects.create(
            name='Fanta', description='Nobody likes it but its still on the market', price=0.99)
        self.kvass = Product.objects.create(
            name='Kvass', description='Just like beer but its not', price=3.00)
        self.watter = Product.objects.create(
            name='Watter', description='Underrated', price=0.50)
        Rule.objects.create(
            rule_type='OL', order_limit=100)
        self.new_cart_item = {
            'product_id': int(self.watter.id),
            'quantity': 3
        }
        self.bad_request = {
            'product_id': 30,
            'quantity': 3
        }
        self.order_limit = {
            'product_id': int(self.fanta.id),
            'quantity': 1000
        }

    def test_add_item_to_cart(self):
        response = self.client.post('/api/cart/item',
                                    data=json.dumps(self.new_cart_item),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_add_item_to_cart_bad_request(self):
        response = self.client.post('/api/cart/item',
                                    data=json.dumps(self.bad_request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_order_limit_reached(self):
        response = self.client.post('/api/cart/item',
                                    data=json.dumps(self.order_limit),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CartItemChangeTest(APITestCase):
    def setUp(self):
        self.cola = Product.objects.create(
            name='Coca Cola', description='Most popular drink', price=1.20)
        self.sprite = Product.objects.create(
            name='Sprite', description='Tastes like lemon', price=1.25)
        self.fanta = Product.objects.create(
            name='Fanta', description='Nobody likes it but its still on the market', price=0.99)
        self.kvass = Product.objects.create(
            name='Kvass', description='Just like beer but its not', price=3.00)
        Cart.objects.create(
            product_id=self.cola, quantity=2)
        Cart.objects.create(
            product_id=self.sprite, quantity=3)
        Cart.objects.create(
            product_id=self.fanta, quantity=10)
        Cart.objects.create(
            product_id=self.kvass, quantity=5)
        self.update_quanity = {
            'product_id': int(self.sprite.id),
            'quantity': 5
        }
        self.bad_request = {
            'product_id': "Fanta",
            'quantity': 10
        }

    def test_update_cart_item(self):
        response = self.client.put('/api/cart/item/' + str(self.sprite.id),
                                    data=json.dumps(self.update_quanity),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_non_existing_cart_item(self):
        response = self.client.put('/api/cart/item/30',
                                    data=json.dumps(self.update_quanity),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_bad_request(self):
        response = self.client.put('/api/cart/item/' + str(self.sprite.id),
                                    data=json.dumps(self.bad_request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_cart_item(self):
        response = self.client.delete('/api/cart/item/' + str(self.sprite.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existing_cart_item(self):
        response = self.client.delete('/api/cart/item/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CartTotalTest(APITestCase):
    def setUp(self):
        self.cola = Product.objects.create(
            name='Coca Cola', description='Most popular drink', price=1.20)
        self.sprite = Product.objects.create(
            name='Sprite', description='Tastes like lemon', price=1.25)
        self.fanta = Product.objects.create(
            name='Fanta', description='Nobody likes it but its still on the market', price=0.99)
        self.kvass = Product.objects.create(
            name='Kvass', description='Just like beer but its not', price=3.00)
        Rule.objects.create(
            rule_type='OL', order_limit=100)
        Rule.objects.create(
            rule_type='PD', product_count=5)
        Rule.objects.create(
            rule_type='OD', order_value=20, discount_on_value=1)
        Rule.objects.create(
            rule_type='OD', order_value=50, discount_on_value=2)
        Cart.objects.create(
            product_id=self.cola, quantity=2)
        Cart.objects.create(
            product_id=self.sprite, quantity=30)
        Cart.objects.create(
            product_id=self.fanta, quantity=10)
        Cart.objects.create(
            product_id=self.kvass, quantity=5)

    def test_get_cart_total(self):
        response = self.client.get('/api/cart/total')
        self.assertEqual(response.status_code, status.HTTP_200_OK)