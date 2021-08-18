# Generated by Django 3.1.7 on 2021-06-12 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shabd', '0023_auto_20210612_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatgroup',
            name='userImage',
        ),
        migrations.AddField(
            model_name='chatgroup',
            name='groupImage',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
