from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверяет наличие прав администратора у пользователя"""

    message = "Access Denied."

    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"


class IsOwner(permissions.BasePermission):
    """Проверяет принадлежность пользователя к запрашиваему объекту"""

    message = "Access Denied. Invalid Credential"

    def has_object_permission(self, request, view, obj):
        result = request.user and request.user.id == obj.pk
        return result


class IsLeadGuide(permissions.BasePermission):
    """Проверяет наличие прав Ведущего Гида у пользователя"""

    message = "Access Denied. Please sign in as lead guide"

    def has_permission(self, request, view):
        return request.user and request.user.role == "lead_guide"


class IsGuide(permissions.BasePermission):
    """Проверяет наличие прав Гида у пользователя"""

    message = "Access Denied. Please sign in as guide."

    def has_permission(self, request, view):
        return request.user and request.user.role == "guide"


class IsUser(permissions.BasePermission):
    """Проверяет наличие подтвержденного email адресса у пользователя"""

    message = (
        "Access Denied. Please confirm your email. "
        "Or you are not actually a regular user. "
    )

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.role == "user"
            and request.user.is_email_confirmed
        )
