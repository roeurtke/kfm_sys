from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import IncomeCategory
from .serializers import IncomeCategorySerializer
from permissions.permissions import HasPermission
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IncomeCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeCategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Define searchable fields
    search_fields = ['name', 'description', 'user__username']

    # Define filterable fields
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'description': ['exact', 'icontains'],
        'status': ['exact'],
        'user__username': ['exact', 'icontains'],
    }
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_income_category')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_income_category')]

    def get_queryset(self):
        # Return all categories for users with permission
        return IncomeCategory.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Income category created successfully", "income_category": response.data}, status=status.HTTP_201_CREATED)

class IncomeCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeCategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_income_category')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_income_category')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_income_category')]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        # Return all categories for users with permission
        return IncomeCategory.objects.all()
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Income category updated successfully.", "income_category": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.status = False
            instance.save()
            return Response({"message": "Income category deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)