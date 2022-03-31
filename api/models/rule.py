from django.db import models
from django.db.models import UniqueConstraint

class Rule(models.Model):
    RULE_TYPES = (
        ('OL', 'ORDER_LIMIT'),
        ('OD', 'ORDER_DISCOUNT'),
        ('PD', 'PRODUCT_DISCOUNT'),
    )

    rule_type = models.CharField(max_length=2, choices=RULE_TYPES)
    order_limit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    order_value = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    discount_on_value = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    product_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.rule_type