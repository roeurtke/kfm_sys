from django.contrib import admin
from .models import Income

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'income_amount', 'currency', 'income_category', 'user', 'status', 'created_at', 'updated_at')  # Fields to display in the list view
    list_filter = ('status', 'income_category', 'user')  # Filters for the list view
    search_fields = ('name', 'description')  # Searchable fields