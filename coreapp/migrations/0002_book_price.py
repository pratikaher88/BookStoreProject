# Generated by Django 2.1.4 on 2018-12-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.IntegerField(default=100, max_length=5),
        ),
    ]
