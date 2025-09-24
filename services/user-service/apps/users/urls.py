from django.urls import path
from .views import UserRegistratedView, UserProfileView, UserUpdateView

urlpatterns = [
    path('register/', UserRegistratedView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserUpdateView.as_view(), name='user-update'),
]
