# Generated by Django 3.1.7 on 2021-04-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shabd', '0002_auto_20210405_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeuserprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
