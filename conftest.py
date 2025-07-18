import pytest
from oauth2_provider.models import Application


@pytest.fixture
def usuario_prueba():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    usuario = User.objects.create_user(
        username="test@ejemplo.com",
        email="test@ejemplo.com",
        password="password123",
        is_active=True,
        is_staff=True,  # Añadimos permisos de staff
    )
    usuario.save()
    return usuario


@pytest.fixture
def aplicacion_oauth():
    return Application.objects.create(
        name="Test Application",
        client_type="confidential",
        authorization_grant_type="password",
        client_id="test-client-id",
        client_secret="test-client-secret",
    )
