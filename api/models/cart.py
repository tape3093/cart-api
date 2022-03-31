from django.db import models
from .product import Product

class Cart(models.Model):
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product