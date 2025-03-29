from rest_framework import serializers
from .models import Income
from income_categories.models import IncomeCategory

class IncomeSerializer(serializers.ModelSerializer):
    income_category = serializers.PrimaryKeyRelatedField(queryset=IncomeCategory.objects.all())  # Allow assigning a category by ID
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Income
        fields = ('id', 'date', 'name', 'description', 'amount', 'currency', 'income_category', 'status', 'user', 'deleted_at', 'created_at', 'updated_at')  # Fields to include in the API
        read_only_fields = ('id', 'user')  # These fields are read-only
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request').method in ['PUT', 'PATCH']:
            self.fields['date'].required = False
            self.fields['name'].required = False
            self.fields['amount'].required = False
            self.fields['income_category'].required = False

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
            "income_category": {
                "id": instance.income_category.id,
                "name": instance.income_category.name,
            } if instance.income_category else None,
            "status": instance.status,
            "user": {
                "id": instance.user.id,
                "username": instance.user.username,
                "email": instance.user.email,
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
            } if instance.user else None
        }