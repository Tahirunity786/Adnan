from rest_framework import serializers
from core_post.models import Save
from django.contrib.auth import get_user_model
from core_post.serializers import UserPostSerializer
from core_profile.models import Story
from core_account.models import interest
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['profile', 'profile_slug', 'profile_info', 'username', 'email', 'date_of_birth']


class GetProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user profiles.
    """
    post = UserPostSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'profile', 'profile_slug', 'profile_info', 'full_name', 'username', 'date_of_birth', 'post']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profiles.
    """
    interest = serializers.PrimaryKeyRelatedField(many=True, queryset=interest.objects.all(),required = False )
    class Meta:
        model = User
        fields = ['email', 'username', 'full_name', 'date_of_birth', 'mobile_number', 'profile', 'profile_info', 'interest']


class UserdSerializer(serializers.Serializer):
    """
    Serializer for user identification.
    """
    user_id = serializers.IntegerField()


class SaveSerializer(serializers.ModelSerializer):
    """
    Serializer for the Save model.
    """
    post = UserPostSerializer(read_only=True, many=True)

    class Meta:
        model = Save
        fields = ['user', 'post', 'date_time']


class StorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Story model.
    """
    class Meta:
        model = Story
        fields = "__all__"