# api/permissions.py
from rest_framework import permissions
from objects.models import ResponsiblePerson

class IsInspectorOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только пользователям с ролью inspector или admin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.role in ('inspector', 'admin'))

class IsAssignedInspectorForObject(permissions.BasePermission):
    """
    Для редактирования конкретного FireObject/InspectionReport проверяем,
    что текущий пользователь — назначенный ответственный (ResponsiblePerson) для объекта
    или имеет роль admin.
    """

    def has_object_permission(self, request, view, obj):
        # admin всегда может
        if getattr(request.user, 'role', None) == 'admin':
            return True

        # Если объект — InspectionReport, возьмём связанный fire_object
        fire_object = getattr(obj, 'fire_object', None) or (obj if hasattr(obj, 'object_type') else None)
        if not fire_object:
            return False

        # проверяем ResponsiblePerson, назначенного за объект (по имени инспектора — можно доработать)
        return ResponsiblePerson.objects.filter(
            fire_object=fire_object,
            name__icontains=request.user.get_full_name()  # упрощённая проверка
        ).exists()
