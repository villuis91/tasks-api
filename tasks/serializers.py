from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_status(self, value):
        if value not in [choice[0] for choice in Task.StatusChoices.choices]:
            raise serializers.ValidationError(
                f"Estado inválido. Opciones válidas: {', '.join([choice[0] for choice in Task.StatusChoices.choices])}"
            )
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
