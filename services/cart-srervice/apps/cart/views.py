from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user_id=self.request.user.id)
        return cart


class CartAddItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user_id=request.user.id)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        price = request.data.get('price')
        product_name = request.data.get('product_name', '')

        if not product_id or not price:
            return Response({'detail': 'product_id и price обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity, 'price': price, 'product_name': product_name}
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartUpdateItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'item_id'

    def get_object(self):
        cart = get_object_or_404(Cart, user_id=self.request.user.id)
        return get_object_or_404(CartItem, id=self.kwargs['item_id'], cart=cart)


class CartRemoveItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'item_id'

    def get_object(self):
        cart = get_object_or_404(Cart, user_id=self.request.user.id)
        return get_object_or_404(CartItem, id=self.kwargs['item_id'], cart=cart)


class CartClearView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user_id=request.user.id)
        cart.clear()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
