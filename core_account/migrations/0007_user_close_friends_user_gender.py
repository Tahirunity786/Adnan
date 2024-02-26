# Generated by Django 5.0.2 on 2024-02-25 18:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_account', '0006_user_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='close_friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], db_index=True, max_length=100, null=True),
        ),
    ]
