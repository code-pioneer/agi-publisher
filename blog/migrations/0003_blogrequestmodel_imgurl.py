# Generated by Django 5.0.2 on 2024-03-22 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogrequestmodel_blogurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogrequestmodel',
            name='imgurl',
            field=models.CharField(max_length=255, null=True),
        ),
    ]