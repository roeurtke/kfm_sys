from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ExpenseCategory
from .serializers import ExpenseCategorySerializer
from permissions.permissions import HasPermission

class ExpenseCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_expense_category')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_expense_category')]
    
    # Return only the expense categories for the current user
    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user)
    
    # Automatically assign the logged-in user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Expense category created successfully", "expense_category": response.data}, status=status.HTTP_201_CREATED)


class ExpenseCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_expense_category')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_expense_category')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_expense_category')]
        return [permissions.IsAuthenticated()]

    # Return only the expense categories for the current user
    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Expense category updated successfully", "expense_category": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.status = False
            instance.save()
            return Response({"message": "Expense category deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)