# Generated by Django 5.0.6 on 2024-06-25 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_cart_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='offer_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='weight',
            name='price',
            field=models.IntegerField(),
        ),
    ]
