# Generated by Django 5.1.7 on 2025-03-17 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_role'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='tbl_users',
        ),
    ]
