# Generated by Django 5.0.6 on 2024-07-02 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_orders_expected_date_orders_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='payment',
            field=models.TextField(default=None, null=True),
        ),
    ]
