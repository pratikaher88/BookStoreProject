# Generated by Django 2.1.4 on 2019-01-12 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0048_auto_20190112_0433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='country',
        ),
    ]
