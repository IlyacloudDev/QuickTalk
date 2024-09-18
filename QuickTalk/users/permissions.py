from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Только владелец объекта (например, пользователь) может редактировать его
        return obj == request.user
