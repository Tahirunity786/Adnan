from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Story(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="User", default="")
    image = models.ImageField(upload_to="usr/story/pic", null=True, blank=True)
    video = models.FileField(upload_to="usr/story/video", null=True, blank=True)