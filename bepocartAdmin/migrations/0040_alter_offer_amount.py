# Generated by Django 5.0.6 on 2024-07-16 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartAdmin', '0039_offer_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]