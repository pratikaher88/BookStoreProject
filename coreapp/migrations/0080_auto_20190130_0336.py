# Generated by Django 2.1.4 on 2019-01-30 03:36

import coreapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0079_auto_20190130_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default=coreapp.models.random_img, upload_to='profile_images/'),
        ),
    ]
