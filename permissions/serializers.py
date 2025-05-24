from rest_framework import serializers
from .models import Permission, RolePermission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'description', 'status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['name'].required = False
            self.fields['codename'].required = False

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.status = validated_data['status']
        
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "codename": instance.codename,
            "description": instance.description,
            "status": instance.status,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ('id', 'role', 'permission', 'status')
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.status = validated_data['status']
        
        instance.save()
        return instance
    
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
            "status": instance.status,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }