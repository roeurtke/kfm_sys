from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from permissions.permissions import HasPermission

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_expense')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_expense')]
    
    # Return only the expenses for the current user
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    # Automatically assign the current user as the owner of the expense
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Expense created successfully", "expense": response.data}, status=status.HTTP_201_CREATED)

class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_expense')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_expense')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_expense')]
        return [permissions.IsAuthenticated()]
    
    # Return only the expenses for the current user
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Expense updated successfully", "expense": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "The expense is deleted."}, status=status.HTTP_200_OK)