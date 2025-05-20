from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Role
from .serializers import RoleSerializer
from permissions.permissions import HasPermission
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all().order_by('-id')
    serializer_class = RoleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Define searchable fields
    search_fields = ['name', 'description']

    # Define filterable fields
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'description': ['exact', 'icontains'],
        'status': ['exact'],
    }

    # Define ordering fields
    # ordering_fields = ['id','name', 'description', 'created_at', 'updated_at']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_role')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_role')]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Role created successfully", "role": response.data}, status=status.HTTP_201_CREATED)

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_role')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_role')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_role')]
        return [permissions.IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Role updated successfully.", "role": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.status = False
            instance.save()
            return Response({"message": "Role deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    