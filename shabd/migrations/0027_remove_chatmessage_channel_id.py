# Generated by Django 3.1.7 on 2021-06-13 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shabd', '0026_auto_20210613_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='channel_id',
        ),
    ]
