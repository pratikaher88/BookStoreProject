# Generated by Django 2.1.4 on 2019-01-05 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0033_auto_20190105_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='book_images/'),
        ),
    ]
