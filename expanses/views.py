from rest_framework import generics, permissions
from .models import Expanse
from .serializers import ExpanseSerializer
from users.models import CustomUser
from permissions.permissions import HasPermission

class ExpanseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpanseSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Return only the expenses for the current user
    def get_queryset(self):
        return Expanse.objects.filter(user=self.request.user)

    # Automatically assign the current user as the owner of the expense
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpanseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpanseSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Return only the expenses for the current user
    def get_queryset(self):
        return Expanse.objects.filter(user=self.request.user)