from django.urls import path
from core_profile.views import (ArchievedPostList, FollowUser, UnfollowUser, FollowersList, FollowingList, Get_profile, Share_profile, UpdateProfile, Close_friend, ReCloseFriend, CloseFriendList, SavedPostList, likePostList)

urlpatterns = [
    # Profile URLs
    path('public/u/profile', Get_profile.as_view(), name="profile-user"),  # Endpoint to retrieve user profile
    path('public/u/profile/update', UpdateProfile.as_view(), name="profile-update"),  # Endpoint to update user profile

    # Follow/Unfollow URLs
    path('public/u/follow', FollowUser.as_view(), name="follow-user"),  # Endpoint to follow a user
    path('public/u/unfollow', UnfollowUser.as_view(), name="unfollow-user"),  # Endpoint to unfollow a user

    # Followers/Following URLs
    path('public/u/follow-list', FollowersList.as_view(), name="followers-list"),  # Endpoint to get followers list
    path('public/u/following-list', FollowingList.as_view(), name="following-list"),  # Endpoint to get following list

    # Close Friends URLs
    path('public/u/show/close-friend', CloseFriendList.as_view(), name="close-friend-list"),  # Endpoint to show close friends list
    path('public/u/make/close-friend', Close_friend.as_view(), name="make-close-friend"),  # Endpoint to add a user as a close friend
    path('public/u/remove/close-friend', ReCloseFriend.as_view(), name="remove-close-friend"),  # Endpoint to remove a user from close friends

    # Share Profile URL
    path('public/u/profile/<str:slug>/share', Share_profile.as_view(), name="share-profile"),  # Endpoint to share user profile

    # Saved Posts URL
    path('public/u/profile/save/post', SavedPostList.as_view(), name="profile-save-post"),  # Endpoint to get saved posts

    # Liked Posts URL
    path('public/u/profile/like/post', likePostList.as_view(), name="profile-like-post"),  # Endpoint to get liked posts

    # Archived Posts URL
    path('public/u/profile/archive/post', ArchievedPostList.as_view(), name="profile-archive-post"),  # Endpoint to get archived posts
]
