from rest_framework import generics, permissions
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenBlacklistSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from .models import CustomUser

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenBlacklistView(TokenBlacklistView):
    serializer_class = CustomTokenBlacklistSerializer

# List all users (GET) and create a new user (POST)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    # Allow unauthenticated access for listing users (GET)
    # Require authentication for creating users (POST)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    # Add context for list views
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'GET':
            context['is_list_view'] = True
        elif self.request.method == 'POST':
            context['is_create'] = True
        return context
    
# Retrieve, update, or delete a specific user (GET, PUT, PATCH, DELETE)
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    # Allow unauthenticated access for retrieving a user (GET)
    # Require authentication for updating or deleting a user (PUT, PATCH, DELETE)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    # Add a context variable to indicate if the operation is an update
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method in ['PUT', 'PATCH']:
            context['is_update'] = True
        return context