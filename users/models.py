from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from roles.models import Role
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'tbl_users'

    def __str__(self):
        return self.username