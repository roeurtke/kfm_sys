from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        db_table = 'tbl_user'  # Custom table name
    
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username