from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated

class UserViewPermission(BasePermission):

    def has_permission(self, request, view):
        if IsAdminUser().has_permission(request, view):
            return True
        if view.action in ['create']:
            return not IsAuthenticated().has_permission(request, view)
        if view.action in ['delete']:
            return IsAdminUser().has_permission(request, view)
        if view.action in ['list','retrieve','update','partial_update']:
            return IsAuthenticated().has_permission(request, view)
        return False

    def has_object_permission(self, request, view, obj):
        if IsAdminUser().has_permission(request, view):
            return True
        if view.action in ['create']:
            return False
        if view.action in ['delete']:
            return IsAdminUser().has_permission(request, view)
        if view.action in ['list','retrieve','update','partial_update']:
            return IsAuthenticated().has_permission(request, view) and request.user == obj
        return False

class AuthTokenPermissions(BasePermission):

    def has_permission(self, request, view):
        if IsAdminUser().has_permission(request, view):
            return True
        if view.action in ['list']:
            return IsAuthenticated().has_permission(request, view)
        if view.action in ['create']:
            return True
        if view.action in ['retrieve']:
            return IsAuthenticated().has_permission(request, view)
        if view.action in ['destroy']:
            return IsAuthenticated().has_permission(request, view)