from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

from .models import Role


class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN or request.user.is_superuser


class IsModeratorOrOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser


class ReviewCommentPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE' and user.role == 'moderator':
            return True
        return user == obj.author
