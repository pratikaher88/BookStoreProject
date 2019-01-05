# Generated by Django 2.1.4 on 2019-01-05 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0029_auto_20190105_0530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercollectionitem',
            name='book',
        ),
        migrations.RemoveField(
            model_name='usercollection',
            name='items',
        ),
        migrations.AddField(
            model_name='usercollection',
            name='books',
            field=models.ManyToManyField(to='coreapp.Book'),
        ),
        migrations.AddField(
            model_name='usercollection',
            name='date_ordered',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coreapp.Profile'),
        ),
        migrations.AlterField(
            model_name='usercollection',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coreapp.Profile'),
        ),
        migrations.DeleteModel(
            name='UserCollectionItem',
        ),
    ]
