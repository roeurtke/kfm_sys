from rest_framework import serializers
from .models import Expense
from expense_categories.models import ExpenseCategory

class ExpenseSerializer(serializers.ModelSerializer):
    expense_category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())  # Allow assigning a category by ID
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Expense
        fields = (
            'id',
            'date',
            'name',
            'description',
            'spent_amount',
            'currency',
            'expense_category',
            'status',
            'user'
        )
        read_only_fields = ('id', 'user')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['name'].required = False
            self.fields['spent_amount'].required = False
            self.fields['expense_category'].required = False

    def validate_amount(self, value):
        """Ensure the amount is non-negative."""
        if value < 0:
            raise serializers.ValidationError({"error": "Amount cannot be negative."})
        return value
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "date": instance.date,
            "name": instance.name,
            "description": instance.description,
            "spent_amount": instance.spent_amount,
            "currency": instance.currency,
            "expense_category": {
                "id": instance.expense_category.id,
                "name": instance.expense_category.name,
            } if instance.expense_category else None,
            "status": instance.status,
            "user": {
                "id": instance.user.id,
                "username": instance.user.username,
                "email": instance.user.email,
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
            } if instance.user else None
        }