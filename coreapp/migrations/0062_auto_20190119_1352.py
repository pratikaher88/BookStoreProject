# Generated by Django 2.1.4 on 2019-01-19 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0061_auto_20190119_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='selleraddress',
            new_name='offerrer_address',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='useraddress',
            new_name='requester_address',
        ),
    ]