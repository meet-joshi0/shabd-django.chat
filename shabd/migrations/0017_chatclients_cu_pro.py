# Generated by Django 3.1.7 on 2021-04-24 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shabd', '0016_auto_20210424_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatclients',
            name='cu_pro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custome_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
