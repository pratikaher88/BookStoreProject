# Generated by Django 2.1.4 on 2019-01-11 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0039_auto_20190111_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='profile',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='coreapp.ShippingAddress'),
        ),
    ]
