from rest_framework import serializers
from .models import Order,OrderItem,Cart,CartItem


class OrderItemserializer(serializers.ModelSerializer):
    class Meta:
        models=OrderItem
        fields=['id','product','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemserializer(read_only=True,many=True)
    
    class Meta:
        models=Order
        fields=['id','user','status','created_at','updated_at','items']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        models=CartItem
        fields=['id','product','quantity']

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(read_only=True,many=True)
    class Meta:
        models=Cart
        fields=['id','user','items']