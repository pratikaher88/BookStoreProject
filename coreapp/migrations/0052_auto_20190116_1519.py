# Generated by Django 2.1.4 on 2019-01-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0051_auto_20190116_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
