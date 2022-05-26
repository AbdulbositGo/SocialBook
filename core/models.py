from django.db import models

# Create your models here.
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4  

# Create your models here.


User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to="profile_images", default="user.png")
    profilebgimg = models.ImageField(upload_to="profile_bg_images", default="bg-image.jpg")
    location = models.CharField(max_length=100, blank=True)
    working_at = models.CharField(max_length=200, blank=True)
    relationship = models.CharField(max_length=50, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    # post_id = models.CharField(max_length=150)
    username = models.CharField(max_length=150)

    
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.profile.user.username} {self.post.user.username} ga \"{self.comment}\"deb yozdi"



class Follow(models.Model):
    user = models.CharField(max_length=100)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user} {self.following}ga obuna bo'ldi"









