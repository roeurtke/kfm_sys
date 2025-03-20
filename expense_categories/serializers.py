from rest_framework import serializers
from .models import ExpenseCategory
from users.models import CustomUser

class ExpenseCategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Allow assigning a user by ID

    class Meta:
        model = ExpenseCategory
        fields = ('id', 'name', 'description', 'master_report', 'status', 'user')  # Fields to include in the API
        read_only_fields = ('id',)  # ID is read-only

    def validate_name(self, value):
        """Ensure the name is unique for the user."""
        user = self.context['request'].user  # Get the current user from the request context
        if ExpenseCategory.objects.filter(name=value, user=user).exists():
            raise serializers.ValidationError("An expense category with this name already exists for the user.")
        return value