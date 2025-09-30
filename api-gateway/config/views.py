import os
import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def _proxy(request, base_url: str, subpath: str) -> HttpResponse:
    url = f"{base_url}/{subpath}"
    method = request.method

    headers = {k: v for k, v in request.headers.items()}
    if 'Host' in headers:
        headers.pop('Host')

    data = request.body if request.body else None
    params = request.GET.dict()

    try:
        resp = requests.request(method, url, headers=headers, params=params, data=data, allow_redirects=True)
        django_resp = HttpResponse(resp.content, status=resp.status_code)
        for k, v in resp.headers.items():
            if k.lower() in ['content-type', 'content-length']:
                django_resp[k] = v
        return django_resp
    except requests.RequestException as e:
        return JsonResponse({'detail': str(e)}, status=502)


@csrf_exempt
def proxy_users(request, path: str):
    return _proxy(request, settings.USER_SERVICE_URL, f"api/users/{path}/")


@csrf_exempt
def proxy_auth(request, path: str):
    return _proxy(request, settings.USER_SERVICE_URL, f"api/auth/{path}/")


@csrf_exempt
def proxy_products(request, path: str):
    return _proxy(request, settings.PRODUCT_SERVICE_URL, f"api/products/{path}/")


@csrf_exempt
def proxy_cart(request, path: str):
    return _proxy(request, settings.CART_SERVICE_URL, f"api/cart/{path}/")


@csrf_exempt
def proxy_products_root(request):
    return _proxy(request, settings.PRODUCT_SERVICE_URL, "api/products/")


@csrf_exempt
def proxy_cart_root(request):
    return _proxy(request, settings.CART_SERVICE_URL, "api/cart/")


