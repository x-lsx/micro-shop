from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok",
                         "service": "user-service"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/auth/', include('apps.authenti.urls')),
    path('health/', health_check, name='health_check')
]
