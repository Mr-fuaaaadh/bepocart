# Generated by Django 5.0.6 on 2024-06-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0013_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
