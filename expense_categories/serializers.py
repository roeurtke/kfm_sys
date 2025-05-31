from rest_framework import serializers
from .models import ExpenseCategory

class ExpenseCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Allow assigning a user by ID

    class Meta:
        model = ExpenseCategory
        fields = (
            'id',
            'name',
            'description',
            'master_report',
            'status',
            'user'
        )  # Fields to include in the API
        read_only_fields = ('id', 'user')  # ID is read-only
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['name'].required = False

    def validate_name(self, value):
        """Ensure the name is globally unique."""
        # Get the current instance if this is an update
        instance = getattr(self, 'instance', None)
        
        # Check if name exists, excluding the current instance if this is an update
        if instance:
            if ExpenseCategory.objects.filter(name=value).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError({"error": "An expense category with this name already exists."})
        else:
            if ExpenseCategory.objects.filter(name=value).exists():
                raise serializers.ValidationError({"error": "An expense category with this name already exists."})
        return value
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        if 'status' in validated_data:
            instance.status = validated_data['status']
            
        instance.save()
        return instance
    
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