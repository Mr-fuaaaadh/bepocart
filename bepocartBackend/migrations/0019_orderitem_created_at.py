# Generated by Django 5.0.6 on 2024-06-29 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartBackend', '0018_remove_customer_username_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]