from django.urls import path
from .views import (
    PermissionListCreateView,
    PermissionRetrieveUpdateDestroyView,
    RolePermissionListCreateView,
    RolePermissionRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('permissions/', PermissionListCreateView.as_view(), name='permission-list-create'),
    path('permissions/<int:pk>/', PermissionRetrieveUpdateDestroyView.as_view(), name='permission-retrieve-update-destroy'),
    path('role-permissions/', RolePermissionListCreateView.as_view(), name='role-permission-list-create'),
    path('role-permissions/<int:pk>/', RolePermissionRetrieveUpdateDestroyView.as_view(), name='role-permission-retrieve-update-destroy'),
]