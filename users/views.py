from rest_framework import generics, permissions, status
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenBlacklistSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import CustomUser
from permissions.permissions import HasPermission
from rest_framework.response import Response

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully", "user": response.data}, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            # Add success message to response data
            response.data["message"] = "Login successful"
            
            # Get refresh token from response data
            refresh_token = response.data.get('refresh')
            
            if refresh_token:
                # Set refresh token in HttpOnly cookie
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,  # For HTTPS (use in production)
                    samesite='Lax',  # or 'Strict' depending on your needs
                    max_age=60 * 60 * 24 * 7,  # 7 days (matches SimpleJWT's default refresh token lifetime)
                )
                
                # Remove refresh token from response body
                del response.data['refresh']
        
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not found.'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['refresh'] = refresh_token
        try:
            return super().post(request, *args, **kwargs)
        except InvalidToken as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
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
        return Response({"message": "User updated successfully", "user": response.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "The user is deleted."}, status=status.HTTP_200_OK)