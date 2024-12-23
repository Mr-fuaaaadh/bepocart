# Generated by Django 5.1 on 2024-09-02 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0036_alter_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(editable=False, max_length=20, null=True, unique=True),
        ),
    ]
