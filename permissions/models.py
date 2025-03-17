from django.db import models
from roles.models import Role

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_permissions'

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')

    class Meta:
        db_table = 'tbl_role_permissions'
        unique_together = ('role', 'permission')  # Ensure each role-permission pair is unique

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"