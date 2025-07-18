from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from oauth2_provider.models import Application
import uuid


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Crear aplicación OAuth2
            client_id = str(uuid.uuid4())
            client_secret = str(uuid.uuid4())

            Application.objects.create(
                user=user,
                name=f'TasksAPI-{user.username}',
                client_id=client_id,
                client_secret=client_secret,
                client_type='confidential',
                authorization_grant_type='password',
                skip_authorization=True
            )

            response_data = {
                "message": "Usuario registrado exitosamente",
                "oauth2_credentials": {
                    "client_id": client_id,
                    "client_secret": client_secret
                },
                "instrucciones": {
                    "obtener_token": {
                        "endpoint": "/o/token/",
                        "method": "POST",
                        "headers": {
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        "body": {
                            "grant_type": "password",
                            "username": user.email,
                            "password": "tu-contraseña",
                            "client_id": client_id,
                            "client_secret": client_secret
                        }
                    }
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
