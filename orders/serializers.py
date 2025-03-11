from rest_framework import serializers
from .models import Order,OrderItem,Cart,CartItem


class OrderItemserializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemserializer(read_only=True,many=True)
    
    class Meta:
        model=Order
        fields=['id','user','status','created_at','updated_at','items']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product','quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Nested serializer for CartItems

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']