from django.contrib import admin
from .models import Expanse

@admin.register(Expanse)
class ExpanseAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'amount', 'currency', 'expense_category', 'user', 'status', 'created_at', 'updated_at')  # Fields to display in the list view
    list_filter = ('status', 'expense_category', 'user')  # Filters for the list view
    search_fields = ('name', 'description')  # Searchable fields