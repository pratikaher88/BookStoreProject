# Generated by Django 2.1.4 on 2019-01-19 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0062_auto_20190119_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='zip_code',
            field=models.CharField(choices=[('421202', '421202'), ('421201', '421201'), ('421204', '421204'), ('421203', '421203'), ('421301', '421301')], default='421202', help_text='we only operate in these locations for now!', max_length=100),
        ),
    ]
