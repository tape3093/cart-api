from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Cart, Product, Rule
from api.serializers import CartSerializer
from drf_spectacular.utils import extend_schema
import math

def get_order_discounts(cart_value):
    try:
        od_rules = Rule.objects.filter(rule_type="OD")
        discount = 0
        for rule in od_rules:
            if cart_value >= rule.order_value:
                discount += float(rule.discount_on_value)
        return discount
    except:
        return 0

def get_product_discounts(cart):
    try:
        pd_rule = Rule.objects.get(rule_type="PD")
        discount = 0
        for item in cart:
            product_price = float(Product.objects.get(pk=item.product_id.id).price)
            discount += math.floor(item.quantity / pd_rule.product_count) * product_price
        return discount
    except:
        return 0

def get_discount_value(cart):
    discount_value = get_product_discounts(cart)
    discount_value += get_order_discounts(get_cart_value(cart))
    return discount_value

def get_cart_value(cart):
    cart_value = 0
    for item in cart:
        product_price = float(Product.objects.get(pk=item.product_id.id).price)
        cart_value += item.quantity * product_price
    return cart_value

def calculate_total(cart):
    return get_cart_value(cart) - get_discount_value(cart)

def order_limit_reached(data):
    try:
        ol_rule = Rule.objects.get(rule_type="OL")
        cart = Cart.objects.all()
        total = calculate_total(cart)

        if total > ol_rule.order_limit:
            return True
    except:
        return False
    return False

class CartList(APIView):
    @extend_schema(request=None, responses=CartSerializer)
    def get(self, request):
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    @extend_schema(request=None, responses=CartSerializer)
    def delete(self, request):
        cart = Cart.objects.all()
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartAdd(APIView):
    @extend_schema(request=CartSerializer,responses=CartSerializer)
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            if order_limit_reached(serializer.data):
                instance.delete()
                return Response({
                    'error': 'Order limit reached'
                }, status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemChange(APIView):
    @extend_schema(request=CartSerializer,responses=CartSerializer)
    def put(self, request, product_id):
        try:
            cart = Cart.objects.get(product_id=product_id)
            serializer = CartSerializer(cart, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'error': 'Item not in cart'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=None,responses=CartSerializer)
    def delete(self, request, product_id):
        try:
            cart = Cart.objects.get(product_id=product_id)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'error': 'Item not in cart'
            }, status=status.HTTP_404_NOT_FOUND)

class CartTotal(APIView):
    @extend_schema(request=None,responses=CartSerializer)
    def get(self, request):
        cart = Cart.objects.all()
        return Response({
            "cart_value": get_cart_value(cart),
            "discount": get_discount_value(cart),
            "total": calculate_total(cart)
        })