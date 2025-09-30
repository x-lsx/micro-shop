from rest_framework import serializers

from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product_id', 'quantity', 'price', 'product_name', 'subtotal')
        read_only_fields = ('subtotal',)

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user_id', 'items', 'total_amount', 'total_items')