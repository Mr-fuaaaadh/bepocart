# Generated by Django 5.1 on 2024-08-31 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0035_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
