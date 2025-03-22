from rest_framework import serializers
from .models import ExpenseCategory

class ExpenseCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Allow assigning a user by ID

    class Meta:
        model = ExpenseCategory
        fields = ('id', 'name', 'description', 'master_report', 'status', 'user')  # Fields to include in the API
        read_only_fields = ('id', 'user')  # ID is read-only
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['name'].required = False

    def validate_name(self, value):
        """Ensure the name is unique for the user."""
        user = self.context['request'].user  # Get the current user from the request context
        if ExpenseCategory.objects.filter(name=value, user=user).exists():
            raise serializers.ValidationError("An expense category with this name already exists for the user.")
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