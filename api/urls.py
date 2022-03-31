from django.contrib import admin
from django.urls import path
from api.views import ProductList, ProductCreate, ProductSingle
from api.views import CartList, CartAdd, CartItemChange, CartTotal
from api.views import CartRuleList, CartRuleCreate, CartRuleChange

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductSingle.as_view()),
    path('product/', ProductCreate.as_view()),

    path('cart/', CartList.as_view()),
    path('cart/item', CartAdd.as_view()),
    path('cart/item/<int:product_id>', CartItemChange.as_view()),
    path('cart/total', CartTotal.as_view()),

    path('cart/rules', CartRuleList.as_view()),
    path('cart/rule', CartRuleCreate.as_view()),
    path('cart/rule/<int:pk>', CartRuleChange.as_view()),
]
