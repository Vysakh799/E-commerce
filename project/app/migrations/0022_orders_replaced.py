# Generated by Django 5.0.6 on 2024-07-05 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='replaced',
            field=models.BooleanField(default=False),
        ),
    ]