# Generated by Django 5.0.2 on 2024-10-16 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_videorequestmodel_transcript_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videorequestmodel',
            name='transcript_url',
        ),
        migrations.AddField(
            model_name='videorequestmodel',
            name='transcript',
            field=models.TextField(max_length=5000, null=True),
        ),
    ]
