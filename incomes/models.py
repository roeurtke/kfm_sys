from django.db import models
from django.utils import timezone
from users.models import CustomUser
from income_categories.models import IncomeCategory

class Income(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    income_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_incomes'  # Custom table name
        verbose_name_plural = 'Incomes'  # Plural name for admin panel

    def __str__(self):
        return self.name  # String representation of the model