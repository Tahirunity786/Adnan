# Generated by Django 5.0.2 on 2024-02-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='usr/story/pic')),
                ('video', models.FileField(blank=True, null=True, upload_to='usr/story/video')),
            ],
        ),
    ]
