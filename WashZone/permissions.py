from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrProvider(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.provider == request.user
