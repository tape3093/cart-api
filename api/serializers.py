from rest_framework import serializers
from api.models import Product, Cart, Rule

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.DjangoModelField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = '__all__'

class RuleSerializer(serializers.ModelSerializer):
    rule_type = serializers.ChoiceField(choices=["OL","OD","PD"])
    order_limit = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    order_value = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    discount_on_value = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    product_count = serializers.IntegerField(required=False)

    class Meta:
        model = Rule
        fields = '__all__'