# Generated by Django 5.0.6 on 2024-07-03 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_orders_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='weight',
            name='stock',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
