# Generated by Django 5.0.6 on 2024-07-08 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartAdmin', '0023_alter_coinvalue_coin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinvalue',
            name='value',
            field=models.FloatField(),
        ),
    ]