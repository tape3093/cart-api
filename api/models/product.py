from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name