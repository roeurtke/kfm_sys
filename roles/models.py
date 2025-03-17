from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_roles'  # Custom table name
        
    def __str__(self):
        return self.name
