# Generated by Django 5.0.4 on 2024-05-27 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image4',
            field=models.FileField(upload_to=''),
        ),
    ]
