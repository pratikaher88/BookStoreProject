# Generated by Django 2.1.4 on 2019-01-05 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='book',
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='coreapp.Book'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]