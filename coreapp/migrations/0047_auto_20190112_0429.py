# Generated by Django 2.1.4 on 2019-01-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0046_shippingaddress_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(default='India', max_length=100, verbose_name='Country'),
        ),
    ]
