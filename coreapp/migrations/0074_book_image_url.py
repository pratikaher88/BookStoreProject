# Generated by Django 2.1.4 on 2019-01-26 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0073_auto_20190125_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]