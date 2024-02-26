# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from core_post.models import Like, Save, UserPost, archive
from core_profile.serializers import (UserSerializer, UserdSerializer, GetProfileSerializer, UserProfileUpdateSerializer, SaveSerializer)
from core_post.serializers import ArchieveSerializer, UserPostSerializer, LikeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import GetProfileSerializer
from core_post.models import UserPost
from rest_framework import generics, permissions
User = get_user_model()

class Get_profile(APIView):
    """
    API endpoint to retrieve user profile details including followers, following, and posts.

    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve user profile details.

        Returns:
            Response: JSON response containing user profile details, followers, following, and posts.
        """

        try:
            # Retrieve authenticated user
            user = User.objects.get(id=request.user.id)

            # Serialize user profile
            profile_serializer = GetProfileSerializer(user)

            # Calculate the number of followers and following
            followers_count = user.followers.count()
            following_count = user.following.count()

            # Retrieve user posts
            posts = UserPost.objects.filter(user=user)

            # Serialize user posts
            post_serializer = UserPostSerializer(posts, many=True)

            # Serialize followers and following
            user_follower = [{"id": follower.id, "username": follower.username} for follower in user.followers.all()]
            user_following = [{"id": following.id, "username": following.username} for following in user.following.all()]

            # Prepare response data
            response = {
                'user_data': profile_serializer.data,
                'follow_data': {
                    'followers_count': followers_count,
                    'following_count': following_count,
                    'user_followers': user_follower,
                    'user_following': user_following
                },
                'user_posts': {
                    "post_count": posts.count(),
                    "post_data": post_serializer.data,
                }  # Serialized posts data
            }
            return Response(response, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class Share_profile(APIView):
    """
    API endpoint to share a user profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        """
        Retrieve and serialize the user profile.

        Parameters:
        - request: The HTTP request object.
        - kwargs: Keyword arguments containing the user profile slug.

        Returns:
        - Response containing the serialized user profile data or error message.
        """
        try:
            slug = kwargs.get('slug')
            post = UserPost.objects.get(post_slug=slug)

            # Serialize the post
            post_data = UserPostSerializer(post)
            return Response(post_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FollowUser(APIView):
    """
    API endpoint to allow a user to follow another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Follow a user.

        Parameters:
        - request: The HTTP request object containing user_id of the user to follow.

        Returns:
        - Response indicating success or failure of the operation.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            try:
                user_to_follow = User.objects.get(id=user_id)
                user = request.user

                # Check if the user is already following user_to_follow
                if user.following.filter(id=user_to_follow.id).exists():
                    return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

                user.following.add(user_to_follow)
                return Response({"success": f"{user} is now following {user_to_follow}"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnfollowUser(APIView):
    """
    API endpoint to allow a user to unfollow another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Unfollow a user.

        Parameters:
        - request: The HTTP request object containing user_id of the user to unfollow.

        Returns:
        - Response indicating success or failure of the operation.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            try:
                user_to_unfollow = User.objects.get(id=user_id)
                user = request.user
                user.following.remove(user_to_unfollow)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowersList(APIView):
    """
    API endpoint to retrieve the list of followers for a user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve and serialize the list of followers for the authenticated user.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response containing the serialized list of followers.
        """
        user = request.user
        followers = user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)


class FollowingList(APIView):
    """
    API endpoint to retrieve the list of users being followed by a user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve and serialize the list of users being followed by the authenticated user.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response containing the serialized list of users being followed.
        """
        user = request.user
        following = user.following.all()
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)
    
class UpdateProfile(APIView):
    """
    API endpoint to allow users to update their profiles.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Update the profile of the authenticated user.
        
        Request Data:
        {
            "full_name": "New Full Name",
            "email": "new@example.com",
            "date_of_birth": "1990-01-01",
            "mobile_number": "1234567890",
            "profile_info": "New profile information"
            # Include any other fields you want to update
        }
        """
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Close_friend(APIView):
    """
    API view to add a user as a close friend.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        POST method to add a user as a close friend.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: Response object with success or error message.

        Raises:
            NotFound: If the user with the provided user_id does not exist.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            try:
                user_close_friend = User.objects.get(id=user_id)
                user = request.user
                # Check if the user is already following user_to_follow
                if user.close_friends.filter(id=user_close_friend.id).exists():
                    return Response({'error': 'You are already close friend of this user'}, status=status.HTTP_400_BAD_REQUEST)
                user.close_friends.add(user_close_friend)
                return Response({"success": f"{user} is now close friend of {user_close_friend}"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CloseFriendList(APIView):
    """
    API view to retrieve the list of close friends for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        GET method to retrieve the list of close friends.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: Response object with the list of close friends.

        """
        user = request.user
        friends = user.close_friends.all()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

class ReCloseFriend(APIView):
    """
    API endpoint to remove a user from the current user's close friends list.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to remove a user from close friends list.

        Parameters:
        - request: HTTP request object
        - *args: Additional positional arguments
        - **kwargs: Additional keyword arguments

        Returns:
        - Response: HTTP response indicating success or failure
        """
        serializer = UserdSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            try:
                user_close_friend = User.objects.get(id=user_id)
                user = request.user
                user.close_friends.remove(user_close_friend)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavedPostList(generics.ListAPIView):
    """
    API endpoint to list all saved posts of the authenticated user.
    """
    serializer_class = SaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve saved posts queryset for the authenticated user.

        Returns:
        - QuerySet: QuerySet of saved posts for the authenticated user
        """
        user = self.request.user
        return Save.objects.filter(user=user)


class likePostList(generics.ListAPIView):
    """
    API endpoint to list all liked posts of the authenticated user.
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve liked posts queryset for the authenticated user.

        Returns:
        - QuerySet: QuerySet of liked posts for the authenticated user
        """
        user = self.request.user
        return Like.objects.filter(user=user)


class ArchievedPostList(generics.ListAPIView):
    """
    API endpoint to list all archived posts of the authenticated user.
    """
    serializer_class = ArchieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve archived posts queryset for the authenticated user.

        Returns:
        - QuerySet: QuerySet of archived posts for the authenticated user
        """
        user = self.request.user
        return archive.objects.filter(user=user)