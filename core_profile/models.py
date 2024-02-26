from django.db import models

# Create your models here.

class Story(models.Model):
    image = models.ImageField(upload_to="usr/story/pic", null=True, blank=True)
    video = models.FileField(upload_to="usr/story/video", null=True, blank=True)