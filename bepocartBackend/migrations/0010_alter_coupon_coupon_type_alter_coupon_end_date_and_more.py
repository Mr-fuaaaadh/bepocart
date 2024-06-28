# Generated by Django 5.0.6 on 2024-06-14 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0009_alter_coupon_discount_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_type',
            field=models.CharField(default='Percentage', max_length=10),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateField(),
        ),
    ]