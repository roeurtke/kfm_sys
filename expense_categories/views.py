from rest_framework import generics, permissions
from .models import ExpenseCategory
from .serializers import ExpenseCategorySerializer
from users.models import CustomUser
from permissions.permissions import HasPermission

class ExpenseCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the expense categories for the current user
        return ExpenseCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the current user as the owner of the expense category
        serializer.save(user=self.request.user)

class ExpenseCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the expense categories for the current user
        return ExpenseCategory.objects.filter(user=self.request.user)