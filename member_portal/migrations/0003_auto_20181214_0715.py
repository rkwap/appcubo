# Generated by Django 2.1.4 on 2018-12-14 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member_portal', '0002_auto_20181214_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed_requests',
            name='comment_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='feed_requests',
            name='downvote_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='comment_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='downvote_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='upvote_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
