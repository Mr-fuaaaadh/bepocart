# Generated by Django 5.0.6 on 2024-05-31 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bepocartAdmin', '0003_remove_category_description_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='studentreg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
