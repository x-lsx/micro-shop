from rest_framework import serializers

from .models import Cart, CartItem

class CartSerializer(serializers.ModelSerializer):

    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        model = Cart
        fields = ('id', 'user_id', 'items', 'total_price')

class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product_id', 'quantity', 'price', 'product_name')