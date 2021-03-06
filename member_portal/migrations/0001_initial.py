# Generated by Django 2.1.2 on 2019-01-01 19:02

from django.db import migrations, models
import member_portal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='feed_requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255)),
                ('appid', models.BigIntegerField(default=None)),
                ('category', models.CharField(choices=[('NR', 'New Release'), ('DI', 'Discovery'), ('UP', 'Update'), ('BF', 'Bugs and Fixes'), ('PD', 'Price Drop')], default=None, max_length=2)),
                ('store', models.CharField(choices=[('AND', 'Android'), ('IOS', 'iOS'), ('UWP', 'UWP'), ('PWA', 'Progressive Web App'), ('LIN', 'Linux'), ('W32', 'Win32'), ('MAC', 'Mac OS')], default=None, max_length=3)),
                ('content', models.TextField(default=None)),
                ('author', models.CharField(default=None, max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sshots', models.ImageField(default=None, null=True, upload_to=member_portal.models.user_directory_path)),
                ('tags', models.TextField(default=None)),
                ('unique_hash', models.CharField(default=None, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='feeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255)),
                ('appid', models.BigIntegerField(default=None)),
                ('category', models.CharField(choices=[('NR', 'New Release'), ('DI', 'Discovery'), ('UP', 'Update'), ('BF', 'Bugs and Fixes'), ('PD', 'Price Drop')], default=None, max_length=2)),
                ('store', models.CharField(choices=[('AND', 'Android'), ('IOS', 'iOS'), ('UWP', 'UWP'), ('PWA', 'Progressive Web App'), ('LIN', 'Linux'), ('W32', 'Win32'), ('MAC', 'Mac OS')], default=None, max_length=3)),
                ('content', models.TextField(default=None)),
                ('author', models.CharField(default=None, max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('sshots', models.ImageField(default=None, null=True, upload_to=member_portal.models.user_directory_path)),
                ('upvote_count', models.IntegerField(blank=True, default=None, null=True)),
                ('downvote_count', models.IntegerField(blank=True, default=None, null=True)),
                ('comment_count', models.IntegerField(blank=True, default=None, null=True)),
                ('upvoters', models.TextField(default=None, null=True)),
                ('downvoters', models.TextField(default=None, null=True)),
                ('tags', models.TextField(default=None)),
                ('dev_response', models.TextField(default=None, null=True)),
                ('unique_hash', models.CharField(default=None, max_length=255, unique=True)),
            ],
        ),
    ]
