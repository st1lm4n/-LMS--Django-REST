from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModeratorOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            # Модераторы могут только читать и обновлять
            return request.method in permissions.SAFE_METHODS + ('PUT', 'PATCH')
        return obj.owner == request.user