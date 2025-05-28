from rest_framework import serializers
from .models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'status', 'created_at', 'updated_at')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['name'].required = False
    
    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.name = validated_data['name']
            instance.description = validated_data['description']
            instance.status = validated_data['status']
            
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "description": instance.description,
            "status": instance.status,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }