# Generated by Django 2.1.4 on 2019-01-03 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0014_auto_20190103_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='Figure_1.png', upload_to='profile_images/'),
        ),
    ]
