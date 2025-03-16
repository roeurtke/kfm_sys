from django.contrib.auth.models import AbstractUser
from django.db import models
from roles.models import Role
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
    # Add a ForeignKey to the Role model (from the role app)
    role = models.ForeignKey(
        Role,  # Reference the Role model in the role app
        on_delete=models.SET_NULL,  # Set role to NULL if the role is deleted
        null=True,
        blank=True,
        related_name='users',  # Allows role.users to access all users with this role
    )
    
    class Meta:
        db_table = 'tbl_user'  # Custom table name
    
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username