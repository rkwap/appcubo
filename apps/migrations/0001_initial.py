# Generated by Django 2.1.2 on 2019-01-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='android',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255)),
                ('publisher', models.CharField(default=None, max_length=300)),
                ('app_url', models.CharField(default=None, max_length=255, unique=True)),
                ('pub_url', models.CharField(default=None, max_length=255)),
                ('cover', models.TextField(default=None)),
                ('price', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='iOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255)),
                ('publisher', models.CharField(default=None, max_length=255)),
                ('app_url', models.CharField(default=None, max_length=255, unique=True)),
                ('publisher_url', models.CharField(default=None, max_length=255)),
                ('cover', models.TextField(default=None)),
                ('price', models.CharField(default=None, max_length=100)),
                ('appid', models.CharField(default=None, max_length=255, unique=True)),
                ('devices', models.CharField(default=None, max_length=200)),
            ],
        ),
    ]
