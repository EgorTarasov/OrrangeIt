# Generated by Django 3.0.5 on 2020-05-31 13:48

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orrangeit_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventinfo',
            name='event_participants',
            field=models.ManyToManyField(default=1, related_name='event_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='eventinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media/my_sell/', location='/Users/dany/Desktop/Python/orrangeit/media/my_sell/'), upload_to='image_directory_path'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media/my_sell/', location='/Users/dany/Desktop/Python/orrangeit/media/my_sell/'), upload_to='gallery_images_directory'),
        ),
    ]
