from rest_framework import permissions


class IsOwnerOrDeny(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsOwnerOrAdminOrModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.role == 'admin' or request.user.role == 'moderator'
