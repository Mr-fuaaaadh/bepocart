# Generated by Django 5.0.6 on 2024-07-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0022_alter_coupon_end_date_alter_coupon_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
