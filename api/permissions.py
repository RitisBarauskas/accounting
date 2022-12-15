from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Разрешения для автора.
    """

    def has_permission(self, request, view):
        return request.user.is_author and request.method in ('PATCH', 'POST', 'GET')

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    """
    Разрешения для администратора.
    """
    def has_permission(self, request, view):
        return request.user.is_admin
