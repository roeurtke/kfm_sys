from rest_framework import generics, permissions
from .models import Role
from .serializers import RoleSerializer
from permissions.permissions import HasPermission

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
    # Allow unauthenticated access for listing users (GET)
    # Require authentication and permission for creating users (POST)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), HasPermission('can_create_role')]

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
    # Allow unauthenticated access for retrieving a user (GET)
    # Require authentication and permission for updating or deleting a user (PUT, PATCH, DELETE)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_role')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_role')]
        return [permissions.IsAuthenticated()]
