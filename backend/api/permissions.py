from rest_framework.permissions import SAFE_METHODS, BasePermission


class BlockedPermission(BasePermission):
    """Проверка заблокирован пользователь."""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )


class AdminOrReadOnly(BasePermission):
    """Создание и изменение для админов"""

    def has_object_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )


class AuthorAdminOrReadOnly(BasePermission):
    """Создание и изменение для админов и автора"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and (
                request.user == obj.author
                or request.user.is_staff
            )
        )
