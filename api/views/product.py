from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Product
from api.serializers import ProductSerializer
from drf_spectacular.utils import extend_schema

class ProductList(APIView):
    @extend_schema(request=None, responses=ProductSerializer)
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductCreate(APIView):
    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductSingle(APIView):
    @extend_schema(request=None, responses=ProductSerializer)
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except:
            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=None, responses=ProductSerializer)
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)