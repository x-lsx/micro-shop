from django.urls import path

from .views import (CategoryListView, SizeListView, ProductListView, ProductDetailView)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("sizes/", SizeListView.as_view(), name="size-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]
