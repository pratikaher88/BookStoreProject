# Generated by Django 2.1.4 on 2019-01-04 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0023_usercollection'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCollectionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('book', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreapp.Book')),
            ],
        ),
        migrations.AlterField(
            model_name='usercollection',
            name='items',
            field=models.ManyToManyField(to='coreapp.UserCollectionItem'),
        ),
    ]
