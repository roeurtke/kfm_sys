# Generated by Django 5.1.7 on 2025-03-20 18:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0002_alter_role_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='role',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
