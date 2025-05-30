from django.db import models
from django.utils import timezone
from users.models import CustomUser

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    master_report = models.BooleanField(default=False)
    status = models.BooleanField(default=True)  # Active/inactive status
    user = models.ForeignKey(
        CustomUser,  # Link to the CustomUser model
        on_delete=models.CASCADE,  # Delete categories if the user is deleted
        related_name='expense_categories'  # Allows user.expense_categories to access all categories for a user
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tbl_expense_categories'  # Custom table name
        verbose_name_plural = 'Expense Categories'  # Plural name for admin panel
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name  # String representation of the model