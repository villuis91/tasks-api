import pytest
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task


@pytest.mark.django_db
class TestTaskAPI:
    def test_listar_tareas(self, api_client, usuario_autenticado):
        Task.objects.create(
            title="Tarea 1",
            description="Descripción 1",
            status=Task.StatusChoices.TODO,
            user=usuario_autenticado,
        )
        Task.objects.create(
            title="Tarea 2",
            description="Descripción 2",
            status=Task.StatusChoices.IN_PROGRESS,
            user=usuario_autenticado,
        )

        response = api_client.get("/api/tasks/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        # Verificar que incluye el estado y su descripción
        assert response.data[0]["status"] in [
            choice[0] for choice in Task.StatusChoices.choices
        ]
        assert "status_display" in response.data[0]

    def test_crear_tarea_con_estado(self, api_client, usuario_autenticado):
        datos = {
            "title": "Nueva Tarea",
            "description": "Descripción de la nueva tarea",
            "status": Task.StatusChoices.IN_PROGRESS,
        }
        response = api_client.post("/api/tasks/", datos)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == Task.StatusChoices.IN_PROGRESS

    def test_crear_tarea_estado_invalido(self, api_client, usuario_autenticado):
        datos = {
            "title": "Nueva Tarea",
            "description": "Descripción de la nueva tarea",
            "status": "ESTADO_INVALIDO",
        }
        response = api_client.post("/api/tasks/", datos)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_actualizar_estado_tarea(self, api_client, usuario_autenticado):
        tarea = Task.objects.create(
            title="Tarea 1", user=usuario_autenticado, status=Task.StatusChoices.TODO
        )

        response = api_client.patch(
            f"/api/tasks/{tarea.id}/", {"status": Task.StatusChoices.FINISHED}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == Task.StatusChoices.FINISHED
