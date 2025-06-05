from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'created_at', 'updated_at')
    # Add created_at and updated_at
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'created_at', 'updated_at')}),  # Add these fields to the edit form
    )
    readonly_fields = ('created_at', 'updated_at')  # Make these fields read-only

admin.site.register(CustomUser, CustomUserAdmin)