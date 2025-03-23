from django.db import models
from django.utils import timezone
from users.models import CustomUser  # Import the CustomUser model

class IncomeCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    master_report = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # Delete categories if the user is deleted
        related_name='income_categories'
    )
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete flag
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_income_categories'
        verbose_name_plural = 'Income Categories'

    def __str__(self):
        return self.name  # String representation of the model