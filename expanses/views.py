from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Expanse
from .serializers import ExpanseSerializer
from users.models import CustomUser
from permissions.permissions import HasPermission

class ExpanseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpanseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_expense')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_expense')]
    
    # Return only the expenses for the current user
    def get_queryset(self):
        return Expanse.objects.filter(user=self.request.user)

    # Automatically assign the current user as the owner of the expense
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Expense created successfully", "expense": response.data}, status=status.HTTP_201_CREATED)

class ExpanseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpanseSerializer
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
        return Expanse.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Expense updated successfully", "expense": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "The expense is deleted."}, status=status.HTTP_200_OK)