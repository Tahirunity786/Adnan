from rest_framework import serializers
from django.contrib.auth import get_user_model
from core_post.models import Comment, Favorite, Like, Save, UserPost, PostImageMedia, PostVideoMedia


User = get_user_model()



class PostImageMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImageMedia
        fields = ['image']

class PostVideoMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideoMedia
        fields = ['video']

class UserPostSerializer(serializers.ModelSerializer):
    images = PostImageMediaSerializer(many=True, required=False)
    videos = PostVideoMediaSerializer(many=True, required=False)

    class Meta:
        model = UserPost
        fields = [ 'user','images', 'videos', 'title', 'description']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for handling likes on posts.
    """
    class Meta:
        model = Like
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for Favorite model.
    """
    class Meta:
        model = Favorite
        fields = '__all__'



class RecursiveCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for recursive comments.
    """
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'timestamp', 'replies']
        read_only_fields = ['user', 'timestamp']

    def get_replies(self, obj):
        """
        Serialize replies to comments recursively.
        """
        replies = obj.replies.all()
        serializer = RecursiveCommentSerializer(replies, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments on posts.
    """
    replies = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'timestamp', 'replies']
        read_only_fields = ['user', 'timestamp']

class SaveSerializer(serializers.ModelSerializer):
    """
    Serializer for saving a post.
    """
    class Meta:
        model = Save
        fields = ['user', 'post', 'date_time']

class UnsaveSerializer(serializers.Serializer):
    """
    Serializer for unsaving a post.
    """
    post_id = serializers.IntegerField(required=True)

    def validate_post_id(self, value):
        """
        Check if the post_id is valid.
        """
        if not UserPost.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid post ID.")
        return value