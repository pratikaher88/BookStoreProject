# Generated by Django 2.1.4 on 2019-01-08 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coreapp', '0034_auto_20190105_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offerrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_from_user', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_to_user', to=settings.AUTH_USER_MODEL)),
                ('requester_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_requester_book_from_user', to='coreapp.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('offerrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
                ('requester_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester_book_from_user', to='coreapp.Book')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flatnumber', models.CharField(max_length=100, verbose_name='Flat Number')),
                ('address1', models.CharField(max_length=200, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=200, verbose_name='Address line 2')),
                ('zip_code', models.CharField(choices=[('421202', '421202'), ('421201', '421201'), ('421203', '421203')], default='421201', max_length=100)),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Shipping Address',
                'verbose_name_plural': 'Shipping Addresses',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('offerer_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerrer_book_from_user', to='coreapp.Book')),
                ('offerrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerrer', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL)),
                ('requester_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_book_from_user', to='coreapp.Book')),
            ],
        ),
    ]