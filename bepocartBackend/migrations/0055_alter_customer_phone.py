# Generated by Django 5.1 on 2024-10-05 09:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0054_merge_0053_address_name_0053_merge_20240913_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must contain only digits.', regex='^\\d+$')]),
        ),
    ]