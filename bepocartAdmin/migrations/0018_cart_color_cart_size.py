# Generated by Django 5.0.6 on 2024-06-21 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartAdmin', '0017_size_producyimage_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bepocartAdmin.producyimage'),
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bepocartAdmin.size'),
        ),
    ]
