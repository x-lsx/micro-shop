from rest_framework import status, generics
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import CustomUser


class LoginView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        mail = request.data.get("mail")
        password = request.data.get("password")
        
        if not mail or not password:
            return Response({"error": "Требуется указать адрес электронной почты и пароль"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(mail=mail, password=password)
        
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "mail": user.mail,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            })
        return Response({"error": "Invalid Credentials"},
                        status=status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Требуется указать refresh токен"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({"access": new_access_token})
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)