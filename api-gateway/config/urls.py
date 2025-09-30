from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from .views import proxy_users, proxy_auth, proxy_products, proxy_cart, proxy_products_root, proxy_cart_root


def health_check(request):
    return JsonResponse({"status": "ok", "service": "api-gateway"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('api/users/<path:path>/', proxy_users),
    path('api/auth/<path:path>/', proxy_auth),
    path('api/products/', proxy_products_root),
    path('api/products/<path:path>/', proxy_products),
    path('api/cart', proxy_cart_root),
    path('api/cart/', proxy_cart_root),
    path('api/cart/<path:path>/', proxy_cart),
]


