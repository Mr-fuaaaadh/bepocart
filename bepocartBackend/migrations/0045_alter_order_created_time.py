# Generated by Django 5.1 on 2024-09-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0044_alter_order_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
