# Generated by Django 5.0.6 on 2024-06-26 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_orders_address_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orders',
            name='outfordelivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orders',
            name='packed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orders',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]