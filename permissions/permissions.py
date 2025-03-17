from rest_framework import permissions

class HasPermission(permissions.BasePermission):
    def __init__(self, permission_codename):
        self.permission_codename = permission_codename

    def has_permission(self, request, view):
        # Check if the user has a role
        if not request.user.role:
            return False
        
        # Check if the user's role has the required permission
        return request.user.role.role_permissions.filter(permission__codename=self.permission_codename).exists()