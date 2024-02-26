from rest_framework import serializers
from django.contrib.auth import get_user_model
from core_post.models import( Comment, Favorite, Like, Save, UserPost, PostImageMedia, PostVideoMedia, archive
)
User = get_user_model()


class PostImageMediaSerializer(serializers.ModelSerializer):
    """
    Serializer for PostImageMedia model.
    """
    class Meta:
        model = PostImageMedia
        fields = ['image']

class PostVideoMediaSerializer(serializers.ModelSerializer):
    """
    Serializer for PostVideoMedia model.
    """
    class Meta:
        model = PostVideoMedia
        fields = ['video']

class UserPostSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPost model.
    """
    # Nested serializer for handling post images
    images = PostImageMediaSerializer(many=True, required=False)
    
    # Nested serializer for handling post videos
    videos = PostVideoMediaSerializer(many=True, required=False)

    class Meta:
        model = UserPost
        fields = ['post_slug','user','images', 'videos', 'title', 'description', 'date', 'likes_count', 'comments_count']


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
        fields = ['id', 'user', 'post', 'content', 'timestamp', 'replies', 'parent_comment']
        read_only_fields = ['user', 'timestamp', 'parent_comment']

class RCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments on posts.
    """
    replies = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'timestamp', 'replies', 'parent_comment']
        read_only_fields = ['user', 'timestamp', 'parent_comment']

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


class CCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model, including replies.

    Attributes:
        replies (serializer.SerializerMethodField): Field to represent replies to the comment.
    """
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'timestamp', 'replies')

    def get_replies(self, obj):
        """
        Method to retrieve replies to a comment.

        Args:
            obj: The comment object.

        Returns:
            list: Serialized data of replies to the comment.
        """
        replies = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(replies, many=True).data

class CLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model.
    """
    class Meta:
        model = Like
        fields = '__all__'


class CommentUserPostSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPost model, including related images, videos, comments, and likes.
    """
    images = PostImageMediaSerializer(many=True, read_only=True)
    videos = PostVideoMediaSerializer(many=True, read_only=True)
    comments = CCommentSerializer(many=True, read_only=True)
    likes = CLikeSerializer(many=True, read_only=True)

    class Meta:
        model = UserPost
        fields = ('images', 'videos', 'title', 'description', 'date', 'likes', 'comments')

class ArchieveSerializer(serializers.ModelSerializer):
    """
    Serializer for handling archive on posts.
    """
    class Meta:
        model = archive
        fields = '__all__'