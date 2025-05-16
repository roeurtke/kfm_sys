from rest_framework import generics, permissions, status
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenBlacklistSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from .models import CustomUser
from permissions.permissions import HasPermission
from rest_framework.response import Response
from django.utils import timezone

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully", "user": response.data}, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data["message"] = "Login successfully"
        return response
        
class CustomTokenBlacklistView(TokenBlacklistView):
    serializer_class = CustomTokenBlacklistSerializer

# List all users (GET) and create a new user (POST)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    # Require authentication and permission for creating users (GET, POST)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_list_user')]
        return [permissions.IsAuthenticated(), HasPermission('can_create_user')]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User created successfully", "user": response.data}, status=status.HTTP_201_CREATED)
    
# Retrieve, update, or delete a specific user (GET, PUT, PATCH, DELETE)
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    # Require authentication and permission for updating or deleting a user (GET, PUT, PATCH, DELETE)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_user')]
        elif self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), HasPermission('can_update_user')]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), HasPermission('can_delete_user')]
        return [permissions.IsAuthenticated()]
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "User updated successfully.", "user": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.status = False
            instance.is_active = False
            instance.save()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)