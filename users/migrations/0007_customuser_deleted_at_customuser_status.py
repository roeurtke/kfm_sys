# Generated by Django 5.1.7 on 2025-05-16 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
