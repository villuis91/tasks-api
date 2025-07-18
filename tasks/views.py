from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET /api/tasks/ - Lista todas las tareas del usuario
    POST /api/tasks/ - Crea una nueva tarea
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/tasks/<id>/ - Obtiene el detalle de una tarea
    PUT /api/tasks/<id>/ - Actualiza una tarea completamente
    PATCH /api/tasks/<id>/ - Actualiza una tarea parcialmente
    DELETE /api/tasks/<id>/ - Elimina una tarea
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")
