# Generated by Django 3.0.5 on 2020-05-31 15:54

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orrangeit_app', '0002_auto_20200531_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media/my_sell/', location='/Users/egortarasov/Documents/Programming /SHP/Prom 2019-2020/orrangeit/media/my_sell/'), upload_to='image_directory_path'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media/my_sell/', location='/Users/egortarasov/Documents/Programming /SHP/Prom 2019-2020/orrangeit/media/my_sell/'), upload_to='gallery_images_directory'),
        ),
    ]
