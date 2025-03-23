from rest_framework import serializers
from .models import IncomeCategory
from users.models import CustomUser

class IncomeCategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Allow assigning a user by ID

    class Meta:
        model = IncomeCategory
        fields = ('id', 'name', 'description', 'master_report', 'status', 'user', 'deleted_at', 'created_at', 'updated_at')  # Fields to include in the API
        read_only_fields = ('id', 'user')  # These fields are read-only
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.context.get('request').method in ['PUT', 'PATCH']:
                self.fields['name'].required = False

    def validate_name(self, value):
        """Ensure the name is unique for the user."""
        user = self.context['request'].user  # Get the current user from the request context
        if IncomeCategory.objects.filter(name=value, user=user).exists():
            raise serializers.ValidationError("An income category with this name already exists for the user.")
        return value
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "description": instance.description,
            "master_report": instance.master_report,
            "status": instance.status,
            "user": {
                "id": instance.user.id,
                "username": instance.user.username,
                "email": instance.user.email,
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
            } if instance.user else None
        }