from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class PostVideoMedia(models.Model):
    """
    Model to represent videos associated with posts.
    """
    video = models.FileField(upload_to="post_videos", verbose_name="Post Video")

class PostImageMedia(models.Model):
    """
    Model to represent images associated with posts.
    """
    image = models.ImageField(upload_to='post_images/', verbose_name="Post Image")

class UserPost(models.Model):
    """
    Model to represent user-created posts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_created", blank=True, null=True)
    images = models.ManyToManyField(PostImageMedia, related_name="posts")
    videos = models.ManyToManyField(PostVideoMedia, related_name="posts", blank=True )
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField(verbose_name="Post Description")
    date = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        """
        String representation of the UserPost object.
        """
        return self.title

    class Meta:
        verbose_name_plural = "User Posts"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "post"),)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "post"),)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "post"),)

