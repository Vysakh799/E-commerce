# Generated by Django 5.0.6 on 2024-06-26 04:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='address_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.addreses'),
        ),
    ]
