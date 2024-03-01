# Generated by Django 5.0.2 on 2024-03-01 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(db_index=True, default='', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='userpost',
            name='Is_allow_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userpost',
            name='allow_comments',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userpost',
            name='hide_likes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userpost',
            name='add_topics',
            field=models.ManyToManyField(blank=True, default='', to='core_post.topics'),
        ),
    ]