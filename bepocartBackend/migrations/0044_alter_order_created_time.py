# Generated by Django 5.1 on 2024-09-05 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0043_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]