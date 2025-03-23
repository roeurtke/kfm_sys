from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import IncomeCategory
from .serializers import IncomeCategorySerializer
from users.models import CustomUser
from permissions.permissions import HasPermission

class IncomeCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_income_category')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_income_category')]

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Income category created successfully", "income_category": response.data}, status=status.HTTP_201_CREATED)

class IncomeCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_income_category')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_income_category')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_income_category')]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Income category updated successfully", "income_category": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "The income category is deleted."}, status=status.HTTP_200_OK)
    