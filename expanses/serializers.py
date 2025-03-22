from rest_framework import serializers
from .models import Expanse
from users.models import CustomUser
from expense_categories.models import ExpenseCategory

class ExpanseSerializer(serializers.ModelSerializer):
    expense_category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())  # Allow assigning a category by ID
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Allow assigning a user by ID

    class Meta:
        model = Expanse
        fields = ('id', 'date', 'name', 'description', 'amount', 'currency', 'expense_category', 'status', 'user')
        read_only_fields = ('id')

    def validate_amount(self, value):
        """Ensure the amount is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        return value