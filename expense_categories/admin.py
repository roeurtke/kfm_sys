from django.contrib import admin
from .models import ExpenseCategory

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'master_report', 'status', 'user')  # Fields to display in the list view
    list_filter = ('status', 'master_report')  # Filters for the list view
    search_fields = ('name', 'description')  # Searchable fields