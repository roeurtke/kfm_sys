from rest_framework import serializers
from .models import Permission, RolePermission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'description')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['name'].required = False
            self.fields['codename'].required = False

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "codename": instance.codename,
            "description": instance.description,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ('id', 'role', 'permission')
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "role": {
                "id": instance.role.id,
                "name": instance.role.name,
                "description": instance.role.description,
            },
            "permission": {
                "id": instance.permission.id,
                "name": instance.permission.name,
                "codename": instance.permission.codename,
                "description": instance.role.description,
            },
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }