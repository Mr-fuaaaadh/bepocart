# Generated by Django 5.0.6 on 2024-07-13 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartAdmin', '0032_alter_product_offer_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='offer_banner',
        ),
        migrations.RemoveField(
            model_name='product',
            name='offer_end_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='offer_start_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='offer_type',
        ),
    ]
