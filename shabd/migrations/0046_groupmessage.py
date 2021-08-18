# Generated by Django 3.2.4 on 2021-07-30 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shabd', '0045_auto_20210710_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(blank=True, max_length=100)),
                ('groupName', models.CharField(blank=True, max_length=100)),
                ('message', models.CharField(max_length=10000, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]