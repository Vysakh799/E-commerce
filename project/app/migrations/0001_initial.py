# Generated by Django 5.0.4 on 2024-05-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField()),
                ('type', models.TextField()),
                ('price', models.TextField()),
                ('offer_price', models.TextField()),
                ('description', models.TextField()),
                ('weight1', models.TextField()),
                ('weight2', models.TextField()),
                ('weight3', models.TextField()),
                ('weight4', models.TextField()),
                ('weight5', models.TextField()),
                ('image1', models.FileField(upload_to='')),
                ('image2', models.FileField(upload_to='')),
                ('image3', models.FileField(upload_to='')),
                ('image4', models.TextField()),
            ],
        ),
    ]