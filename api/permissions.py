from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Разрешения для автора.
    """

    def has_permission(self, request, view):
        return request.method in ('PATCH', 'POST', 'GET') and request.user.is_authenticated and request.user.is_author

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    """
    Разрешения для администратора.
    """
    def has_permission(self, request, view):
        return request.method in ('PATCH', 'GET') and request.user.is_authenticated and request.user.is_admin
