import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAutenticacion:
    def test_registro_usuario(self, client):
        # Este test ya está pasando, lo dejamos igual
        url = reverse("register")
        datos = {
            "username": "nuevo_usuario",
            "email": "nuevo@ejemplo.com",
            "password": "Contraseña123",
            "password_confirmation": "Contraseña123",
            "first_name": "Nuevo",
            "last_name": "Usuario",
        }
        response = client.post(url, datos)
        assert response.status_code == status.HTTP_201_CREATED
