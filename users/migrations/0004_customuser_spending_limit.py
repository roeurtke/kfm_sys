# Generated by Django 5.1.7 on 2025-03-20 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='spending_limit',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='The maximum amount the user can spend.', max_digits=10),
        ),
    ]
