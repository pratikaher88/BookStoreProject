# Generated by Django 2.1.4 on 2019-01-20 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0067_auto_20190119_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.IntegerField(blank=True, help_text='We would be deducting 20 rupees from item price for delivery purposes.', null=True),
        ),
    ]