# Generated by Django 5.1 on 2024-09-21 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0052_alter_customer_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
