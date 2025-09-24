from .models import CustomUser
from .serializers import UserSerializer, UserRegistrationsSerializers, UserUpdateSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class UserRegistratedView(generics.CreateAPIView):
    
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationsSerializers
    permission_classes = []
    
class UserProfileView(generics.RetrieveAPIView):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateView(generics.RetrieveUpdateAPIView):

    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    