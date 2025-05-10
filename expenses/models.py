from django.db import models
from django.utils import timezone
from users.models import CustomUser  # Import the CustomUser model
from expense_categories.models import ExpenseCategory  # Import the ExpenseCategory model

class Expense(models.Model):
    date = models.DateField()  # Date of the expense
    name = models.CharField(max_length=255)  # Name of the expense
    description = models.TextField(blank=True, null=True)  # Optional description
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the expense
    currency = models.CharField(max_length=3, default='USD')  # Currency code (e.g., USD, EUR)
    expense_category = models.ForeignKey(
        ExpenseCategory,  # Link to the ExpenseCategory model
        on_delete=models.CASCADE,  # Delete expenses if the category is deleted
        related_name='expenses'  # Allows category.expenses to access all expenses for a category
    )
    status = models.BooleanField(default=True)  # Active/inactive status
    user = models.ForeignKey(
        CustomUser,  # Link to the CustomUser model
        on_delete=models.CASCADE,  # Delete expenses if the user is deleted
        related_name='expenses'  # Allows user.expenses to access all expenses for a user
    )
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete flag
    created_at = models.DateTimeField(default=timezone.now)  # Automatically set when the record is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated when the record is modified

    class Meta:
        db_table = 'tbl_expenses'  # Custom table name
        verbose_name_plural = 'Expenses'  # Plural name for admin panel

    def __str__(self):
        return self.name  # String representation of the model