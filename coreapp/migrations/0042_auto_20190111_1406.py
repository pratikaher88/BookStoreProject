# Generated by Django 2.1.4 on 2019-01-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0041_auto_20190111_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='address1',
            field=models.CharField(max_length=500, verbose_name='Address line 1'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address2',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Address line 2'),
        ),
    ]
