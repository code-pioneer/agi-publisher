# Generated by Django 5.0.2 on 2024-10-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_videotaskmodel_delete_videothememodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='videorequestmodel',
            name='image_prompt',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='videorequestmodel',
            name='voice',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
