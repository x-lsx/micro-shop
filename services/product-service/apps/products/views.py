from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters

from .serializers import (CategorySerializer, SizeSerializer,
                          ProductImageSerializer,ProductCartSerializer,
                          ProductSizeSerializer, ProductDetailSerializer)

from .models import (Category, Size, 
                     Product, ProductSize,
                     ProductImage)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
class SizeListView(generics.ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)

        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer