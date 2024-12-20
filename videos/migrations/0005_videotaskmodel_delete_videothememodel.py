# Generated by Django 5.0.2 on 2024-10-17 03:47

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_remove_videorequestmodel_transcript_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTaskModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=40, null=True)),
                ('ts', models.DateTimeField(auto_now=True)),
                ('video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.videorequestmodel')),
            ],
        ),
        migrations.DeleteModel(
            name='VideoThemeModel',
        ),
    ]
