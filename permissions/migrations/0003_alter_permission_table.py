# Generated by Django 5.1.7 on 2025-03-17 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_alter_rolepermission_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='permission',
            table='tbl_permissions',
        ),
    ]
