# Generated by Django 5.0.6 on 2024-07-10 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartAdmin', '0028_alter_product_slug_alter_subcategory_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producyimage',
            name='size',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]