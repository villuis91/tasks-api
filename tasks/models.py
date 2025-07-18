from django.db import models
from django.conf import settings


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        TODO = "TODO", "Por hacer"
        IN_PROGRESS = "IN_PROGRESS", "En progreso"
        FINISHED = "FINISHED", "Terminada"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
