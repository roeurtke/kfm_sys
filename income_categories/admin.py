from django.contrib import admin
from .models import IncomeCategory

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'master_report', 'status', 'user', 'created_at', 'updated_at')  # Fields to display in the list view
    list_filter = ('status', 'master_report')  # Filters for the list view
    search_fields = ('name', 'description')  # Searchable fields