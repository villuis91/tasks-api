from django.contrib import admin
from .models import Task
from core.models import User


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at", "user")
    search_fields = ("title", "description", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Información Principal", {"fields": ("title", "description", "user")}),
        ("Estado", {"fields": ("status",)}),
        (
            "Información Temporal",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        """
        Si el usuario no es superusuario, solo ve sus propias tareas
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Limita las opciones del campo user a solo usuarios activos
        """
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Si no se especifica un usuario, usa el usuario actual
        """
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)
