# Generated by Django 5.1 on 2024-09-03 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0036_alter_order_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='razorpay_order_id',
        ),
    ]
