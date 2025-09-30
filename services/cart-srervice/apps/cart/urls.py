from django.urls import path

from .views import (
    CartDetailView,
    CartAddItemView,
    CartUpdateItemView,
    CartRemoveItemView,
    CartClearView,
)

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('items/', CartAddItemView.as_view(), name='cart-add-item'),
    path('items/<int:item_id>/', CartUpdateItemView.as_view(), name='cart-update-item'),
    path('items/<int:item_id>/delete/', CartRemoveItemView.as_view(), name='cart-remove-item'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
]


