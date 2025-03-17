"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    CustomTokenBlacklistView,
)

# Swagger/OpenAPI documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="User API",
        default_version='v1',
        description="User authentication API",
    ),
    public=True,
)

urlpatterns = [
     # Admin panel
    path('admin/', admin.site.urls),

    # Authentication endpoints
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', CustomTokenBlacklistView.as_view(), name='logout'),

    # API documentation (Swagger/Redoc)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # User CRUD endpoints
    path('api/users/', include('users.urls')),
    
    # Role CRUD endpoints
    path('api/roles/', include('roles.urls')),
    
    # Permission CRUD endpoints
    path('api/', include('permissions.urls')),
]
