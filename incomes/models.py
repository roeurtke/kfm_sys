from django.db import models
from django.utils import timezone
from users.models import CustomUser  # Import the CustomUser model
from income_categories.models import IncomeCategory  # Import the IncomeCategory model

class Income(models.Model):
    date = models.DateField()  # Date of the income
    name = models.CharField(max_length=255)  # Name of the income
    description = models.TextField(blank=True, null=True)  # Optional description
    income_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the income
    currency = models.CharField(max_length=3, default='USD')  # Currency code (e.g., USD, EUR)
    income_category = models.ForeignKey(
        IncomeCategory,  # Link to the IncomeCategory model
        on_delete=models.CASCADE,  # Delete incomes if the category is deleted
        related_name='incomes'  # Allows category.incomes to access all incomes for a category
    )
    status = models.BooleanField(default=True)  # Active/inactive status
    user = models.ForeignKey(
        CustomUser,  # Link to the CustomUser model
        on_delete=models.CASCADE,  # Delete incomes if the user is deleted
        related_name='incomes'  # Allows user.incomes to access all incomes for a user
    )
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete flag
    created_at = models.DateTimeField(default=timezone.now)  # Automatically set when the record is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated when the record is modified

    class Meta:
        db_table = 'tbl_incomes'  # Custom table name
        verbose_name_plural = 'Incomes'  # Plural name for admin panel

    def __str__(self):
        return self.name  # String representation of the model