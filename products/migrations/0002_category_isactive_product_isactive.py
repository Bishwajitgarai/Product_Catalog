# Generated by Django 5.1.2 on 2024-11-01 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
