from django.urls import path
from core_post.views import (UserPostCreateView, UserPostDeleteView, UserPostUpdateView, LikeDeleteView, CommentCreateView, CommentsonCommentCreateView, UserPostFavoriteView, UserPostFavoriteDeleteView, LikeCreateView, SavePostView, UnsavePostView)

urlpatterns = [
    path("public/post/create", UserPostCreateView.as_view(), name="new-post-create"),
    path("public/post/delete", UserPostDeleteView.as_view(), name="new-post-delete"),
    path("public/post/update", UserPostUpdateView.as_view(), name="new-post-update"),
    path("public/post/favourite/delete", UserPostFavoriteDeleteView.as_view(), name="post-fave-del"),
    path("public/post/favourite/create", UserPostFavoriteView.as_view(), name="post-fave"),
    path("public/post/comments-on-comments", CommentsonCommentCreateView.as_view(), name="comments-on-comments"),
    path("public/post/comment", CommentCreateView.as_view(), name="comments"),
    path("public/post/like", LikeCreateView.as_view(), name="post-like"),
    path("public/post/like/delete", LikeDeleteView.as_view(), name="post-like-delete"),
    path("public/post/save", SavePostView.as_view(), name="post-save"),
    path("public/post/save/delete", UnsavePostView.as_view(), name="post-save-del"),
    
]
