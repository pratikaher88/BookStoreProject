# Generated by Django 2.1.4 on 2019-01-04 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0020_auto_20190104_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_images/'),
        ),
    ]
