# Generated by Django 3.1.7 on 2021-06-12 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shabd', '0021_auto_20210601_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.AlterField(
            model_name='customeuserprofile',
            name='userImage',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
