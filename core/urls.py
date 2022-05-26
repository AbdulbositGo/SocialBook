from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="index"),
    path("upload", upload, name="upload"),
    path("update-post/<uuid:post_id>", update_post, name="update-post"),
    path("delete-post/<uuid:post_id>", delete_post, name="delete-post"),
    path("upload", upload, name="upload"),
    path("comment<uuid:post_id>", comment, name="comment"),
    path("profile/<str:user_id>", profile, name="profile"),
    path("follow", follow, name="follow"),
    path("like-post", like_post, name="like-post"),
    path("settings", settings, name="settings"),
    path("signup", signup, name="signup"),
    path("signin", signin, name="signin"),
    path("logout", logout, name="logout"),
]