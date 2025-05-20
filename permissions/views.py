from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Permission, RolePermission
from .serializers import PermissionSerializer, RolePermissionSerializer
from permissions.permissions import HasPermission
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PermissionListCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all().order_by('-id')
    serializer_class = PermissionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Define searchable fields
    search_fields = ['name', 'codename', 'description']

    # Define filterable fields
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'codename': ['exact', 'icontains'],
        'description': ['exact', 'icontains'],
        'status': ['exact'],
    }

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_permission')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_permission')]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Permission created successfully", "permission": response.data}, status=status.HTTP_201_CREATED)

class PermissionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_permission')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_permission')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_permission')]
        return [permissions.IsAuthenticated()]
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Permission updated successfully.", "permission": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.status = False
            instance.save()
            return Response({"message": "Permission deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RolePermissionListCreateView(generics.ListCreateAPIView):
    queryset = RolePermission.objects.all().order_by('-id')
    serializer_class = RolePermissionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Define searchable fields
    search_fields = ['id', 'role__id', 'permission__id', 'role__name', 'permission__name']

    # Define filterable fields
    filterset_fields = {
        'role': ['exact'],
        'role__id': ['exact'],
        'role__name': ['exact', 'icontains'],
        'permission': ['exact'],
        'permission__id': ['exact'],
        'permission__name': ['exact', 'icontains'],
    }

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_role_permission')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_role_permission')]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Role and Permission created successfully", "role_permission": response.data}, status=status.HTTP_201_CREATED)

class RolePermissionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_role_permission')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_role_permission')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_role_permission')]
        return [permissions.IsAuthenticated()]
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Role and Permission updated successfully.", "role_permission": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.status = False
            instance.save()
            return Response({"message": "Role and Permission deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)