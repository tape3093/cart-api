import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import Product
from ..serializers import ProductSerializer


client = APIClient()

class ProductListTest(APITestCase):
    def setUp(self):
        Product.objects.create(
            name='Coca Cola', description='Most popular drink', price=1.20)
        Product.objects.create(
            name='Sprite', description='Tastes like lemon', price=1.25)
        Product.objects.create(
            name='Fanta', description='Nobody likes it but its still on the market', price=0.99)
        Product.objects.create(
            name='Kvass', description='Just like beer but its not', price=3.00)

    def test_get_all(self):
        response = self.client.get('/api/products/')
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductCreateTest(APITestCase):
    def setUp(self):
        self.valid_product = {
            'name': 'Water',
            'description': 'Very good water',
            'price': 0.80
        }
        self.bad_request = {
            'name': 'Shweps',
            'price': "5"
        }

    def test_create_product(self):
        response = self.client.post('/api/product/', 
                                    data=json.dumps(self.valid_product),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_bad_request(self):
        response = self.client.post('/api/product/', 
                                    data=json.dumps(self.bad_request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProductSingleTest(APITestCase):
    def setUp(self):
        self.cola = Product.objects.create(
            name='Coca Cola', description='Most popular drink', price=1.20)
        self.sprite = Product.objects.create(
            name='Sprite', description='Tastes like lemon', price=1.25)
        self.fanta = Product.objects.create(
            name='Fanta', description='Nobody likes it but its still on the market', price=0.99)
        self.kvass = Product.objects.create(
            name='Kvass', description='Just like beer but its not', price=3.00)
        self.new_fanta_price = {
            'name': 'Fanta',
            'description': 'Nobody likes it but its still on the market',
            'price': 1.20
        }
        self.bad_request = {
            'name': 'Fanta',
            'description': 100,
            'price': "test"
        }

    def test_get_valid_single_product(self):
        response = self.client.get('/api/products/' + str(self.cola.pk))
        cola = Product.objects.get(pk=self.cola.pk)
        serializer = ProductSerializer(cola)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = self.client.get('/api/products/10')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_single_product(self):
        response = self.client.put('/api/products/' + str(self.fanta.pk),
                                    data=json.dumps(self.new_fanta_price),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_non_existing_product(self):
        response = self.client.put('/api/products/30',
                                    data=json.dumps(self.new_fanta_price),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_bad_request(self):
        response = self.client.put('/api/products/' + str(self.fanta.pk),
                                    data=json.dumps(self.bad_request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_single_product(self):
        response = self.client.delete('/api/products/' + str(self.kvass.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existing_product(self):
        response = self.client.delete('/api/products/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)