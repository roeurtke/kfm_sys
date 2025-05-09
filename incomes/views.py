from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Income
from .serializers import IncomeSerializer
from permissions.permissions import HasPermission

class IncomeListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_income')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_income')]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Income created successfully", "income": response.data}, status=status.HTTP_201_CREATED)

class IncomeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_income')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_income')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_income')]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Income updated successfully", "income": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "The  is deleted."}, status=status.HTTP_200_OK)