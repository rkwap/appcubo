# Generated by Django 2.1.2 on 2019-01-05 21:12

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member_portal', '0003_auto_20190105_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed_requests',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='feeds',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
