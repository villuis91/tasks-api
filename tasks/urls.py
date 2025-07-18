from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path("api/tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("api/tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
