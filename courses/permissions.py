from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        # Требуем аутентификацию для всех действий
        if not request.user.is_authenticated:
            return False

        if view.action == 'create':
            return True

        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        if request.user.groups.filter(name='moderators').exists():
            return True
        return False