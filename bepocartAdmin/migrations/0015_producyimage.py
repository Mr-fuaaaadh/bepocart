# Generated by Django 5.0.6 on 2024-06-10 04:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartAdmin', '0014_cart_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProducyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='product/Images')),
                ('image2', models.ImageField(upload_to='product/Images')),
                ('image3', models.ImageField(upload_to='product/Images')),
                ('image4', models.ImageField(upload_to='product/Images')),
                ('image5', models.ImageField(upload_to='product/Images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='bepocartAdmin.product')),
            ],
            options={
                'db_table': 'ProductImage',
            },
        ),
    ]
