# Generated by Django 5.0.4 on 2024-06-18 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_rename_contact_contacts'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.TextField()),
                ('p_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('w_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.weight')),
            ],
        ),
    ]