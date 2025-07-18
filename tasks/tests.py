import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


@pytest.mark.django_db
class TestTaskAPI:
    @pytest.fixture
    def usuario1(self):
        return User.objects.create_user(
            username='usuario1',
            password='contraseña123',
            email='usuario1@test.com'
        )

    @pytest.fixture
    def usuario2(self):
        return User.objects.create_user(
            username='usuario2',
            password='contraseña123',
            email='usuario2@test.com'
        )

    @pytest.fixture
    def token_usuario1(self, usuario1):
        from oauth2_provider.models import Application, AccessToken
        from django.utils import timezone
        import datetime

        # Crear aplicación OAuth2
        app = Application.objects.create(
            name="Test App",
            client_type="confidential",
            authorization_grant_type="password",
            user=usuario1,
        )

        # Crear token
        return AccessToken.objects.create(
            user=usuario1,
            application=app,
            token="token-usuario1",
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write",
        )

    @pytest.fixture
    def token_usuario2(self, usuario2):
        from oauth2_provider.models import Application, AccessToken
        from django.utils import timezone
        import datetime

        app = Application.objects.create(
            name="Test App 2",
            client_type="confidential",
            authorization_grant_type="password",
            user=usuario2,
        )

        return AccessToken.objects.create(
            user=usuario2,
            application=app,
            token="token-usuario2",
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write",
        )

    def test_crear_tarea(self, client, token_usuario1):
        """Test para crear una nueva tarea"""
        datos = {
            "title": "Nueva Tarea",
            "description": "Descripción de la tarea",
            "status": Task.StatusChoices.TODO,
        }

        response = client.post(
            "/api/tasks/",
            data=datos,
            HTTP_AUTHORIZATION=f"Bearer {token_usuario1.token}",
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1
        tarea = Task.objects.first()
        assert tarea.title == "Nueva Tarea"
        assert tarea.user == token_usuario1.user

    def test_listar_tareas(self, client, token_usuario1, usuario1):
        """Test para listar tareas del usuario"""
        # Crear algunas tareas para el usuario
        Task.objects.create(title="Tarea 1", user=usuario1)
        Task.objects.create(title="Tarea 2", user=usuario1)
        Task.objects.create(title="Tarea 3", user=usuario1)

        response = client.get(
            "/api/tasks/", HTTP_AUTHORIZATION=f"Bearer {token_usuario1.token}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        assert all(tarea["title"].startswith("Tarea") for tarea in response.data)

    def test_no_acceso_tareas_otro_usuario(
        self, client, token_usuario1, token_usuario2, usuario2
    ):
        """Test para verificar que un usuario no puede acceder a las tareas de otro"""
        # Crear tarea para usuario2
        tarea = Task.objects.create(title="Tarea de Usuario 2", user=usuario2)

        # Intentar acceder con usuario1
        response = client.get(
            f"/api/tasks/{tarea.id}/",
            HTTP_AUTHORIZATION=f"Bearer {token_usuario1.token}",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_token_invalido(self, client):
        """Test para verificar que no se puede acceder con un token inválido"""
        # Intentar acceder con token inválido
        response = client.get("/api/tasks/", HTTP_AUTHORIZATION="Bearer token-invalido")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_sin_token(self, client):
        """Test para verificar que no se puede acceder sin token"""
        response = client.get("/api/tasks/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_expirado(self, client, usuario1):
        """Test para verificar que no se puede acceder con un token expirado"""
        from oauth2_provider.models import Application, AccessToken
        from django.utils import timezone
        import datetime

        app = Application.objects.create(
            name="Test App",
            client_type="confidential",
            authorization_grant_type="password",
            user=usuario1,
        )

        # Crear token expirado
        token_expirado = AccessToken.objects.create(
            user=usuario1,
            application=app,
            token="token-expirado",
            expires=timezone.now() - datetime.timedelta(days=1),
            scope="read write",
        )

        response = client.get(
            "/api/tasks/", HTTP_AUTHORIZATION=f"Bearer {token_expirado.token}"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
