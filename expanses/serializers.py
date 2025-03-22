from rest_framework import serializers
from .models import Expanse
from users.models import CustomUser
from expense_categories.models import ExpenseCategory

class ExpanseSerializer(serializers.ModelSerializer):
    expense_category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())  # Allow assigning a category by ID
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Expanse
        fields = ('id', 'date', 'name', 'description', 'amount', 'currency', 'expense_category', 'status', 'user')
        read_only_fields = ('id',)

    def validate_amount(self, value):
        """Ensure the amount is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        return value
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "date": instance.date,
            "name": instance.name,
            "description": instance.description,
            "amount": instance.amount,
            "currency": instance.currency,
            "expense_category": instance.expense_category.id,
            "status": instance.status,
            "user": {
                "id": instance.user.id,
                "username": instance.user.username,
                "email": instance.user.email,
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
            } if instance.user else None
        }