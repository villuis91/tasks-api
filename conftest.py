import pytest
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application


@pytest.fixture
def usuario_prueba():
    User = get_user_model()
    return User.objects.create_user(
        username='usuario_test',
        email='test@ejemplo.com',
        password='password123'
    )


@pytest.fixture
def aplicacion_oauth():
    return Application.objects.create(
        name='Test Application',
        client_type='confidential',
        authorization_grant_type='password',
        client_id='test-client-id',
        client_secret='test-client-secret'
    )
