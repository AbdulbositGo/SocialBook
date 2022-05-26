from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *



@login_required(login_url="signin")
def index(request):
    context = {}
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    user_following = Follow.objects.filter(user=request.user)
    my_likes = Like.objects.filter(username=request.user.username)


    user_following_post = []
    for i in range(len(user_following)):
        user_following_post += Post.objects.filter(user__username = user_following[i].following)

    user_following_post += Post.objects.filter(user__username = request.user.username)

    user_following_post_comments = []
    for i in range(len(user_following_post)):
        comment = Comment.objects.filter(post=user_following_post[i])
        if comment:
            user_following_post_comments += comment


    rec_users = Profile.objects.all().order_by("?")

    context["user_profile"] = user_profile
    context["user_following_post"] = user_following_post
    context["user_following_post_comments"] = user_following_post_comments
    context["rec_users"] = rec_users[:4]
    context["my_likes"] = my_likes


    return render(request, "index.html", context)



@login_required(login_url="signin")
def upload(request):
    if request.method == "POST":

        upload_image = request.FILES.get("upload_image")
        if not upload_image:
            messages.info(request, "Post uchun rasm yuklash shart")
            return redirect("upload")

        user_object = User.objects.get(username=request.user.username)
        profile_object = Profile.objects.get(user=user_object)
        caption = request.POST.get("caption")

        post = Post(user=user_object, profile=profile_object, image=upload_image, caption=caption)
        post.save()
        return redirect("/")

    else:
        return redirect("/")


def update_post(request, post_id):
    return


def delete_post(request, post_id):

    post_obj = Post.objects.get(id=post_id)
    if not post_obj:
        return redirect("/")

    else:
        post_obj.delete()
        messages.info(request, "post o'chirildi")
        return redirect("/profile/" + request.user.username)


@login_required(login_url="signin")
def comment(request, post_id):
    if request.method == "POST":
        post = post_id
        user_obj = User.objects.get(username=request.user.username)

        comment = str(request.POST.get("comment"))
        
        if comment.isspace() or not post:
            return redirect("/")
        
        post_object = Post.objects.get(id=post)
        profile_object = Profile.objects.get(user=user_obj)
        
        if post_object and profile_object:
            new_comment = Comment(post=post_object, profile=profile_object, comment=comment)
            new_comment.save()

    return redirect("/")


@login_required(login_url="signin")
def profile(request, user_id):
    context = {}

    user_object = User.objects.get(username=user_id)
    profile_object = Profile.objects.get(user=user_object)
    post_objects = Post.objects.filter(profile=profile_object)
    current_user_following = Follow.objects.filter(user=user_id)
    current_user_followers = Follow.objects.filter(following=profile_object)

    current_user = request.user.username

    if Follow.objects.filter(user=current_user, following=profile_object).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"


    context["profile_object"] = profile_object
    context["post_objects"] = post_objects
    context["post_objects_len"] = len(post_objects)
    context["button_text"] = button_text
    context["current_user_followers"] = len(current_user_followers)
    context["current_user_following"] = len(current_user_following)

    return render(request, "profile.html", context)


@login_required(login_url="signin")
def follow(request):

    if request.method == "POST":
        following_profile = Profile.objects.get(id=request.POST.get("following"))

        new_follow = Follow.objects.filter(user=request.user.username, following=following_profile).first()
        if new_follow:
            new_follow.delete()
        else:
            new_follow = Follow(user=request.user.username, following=following_profile)
            new_follow.save()
    
        return redirect("/profile/" + following_profile.user.username)

    else:
        return redirect("/")


@login_required(login_url="singin")
def like_post(request):

    username = request.user.username
    post_id = request.GET.get("post_id")
    if not post_id:
        return redirect("/")
    post_object = Post.objects.get(id=post_id)


    liked_post = Like.objects.filter(username=username, post_id=post_object).first()
    if not liked_post:
        liked_post = Like(username=username, post_id=post_object)
        liked_post.save()
        post_object.likes += 1
        post_object.save()
        return redirect('/')

    else:
        liked_post.delete()
        post_object.likes -= 1
        post_object.save()
        return redirect('/')


@login_required(login_url="signin")
def settings(request):
    context = {}

    user_profile = Profile.objects.filter(user=request.user).first()

    if request.method=="POST":
        
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        bio = request.POST.get("bio")
        location = request.POST.get("location")
        working_at = request.POST.get("working_at")
        relationship = request.POST.get("relationship")

        user = User.objects.get(username=request.user.username)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        if request.FILES.get("profileimg"):
            image = request.FILES.get("profileimg")
            user_profile.profileimg = image

        user_profile.firstname = user.first_name
        user_profile.lastname = user.last_name
        user_profile.bio = bio
        user_profile.location = location
        user_profile.working_at = working_at
        user_profile.relationship = relationship
        user_profile.save()
        return redirect("/")    

    context["user_profile"] = user_profile      

    return render(request, "setting.html", context)


def signup(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "This username is busy")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "This email is busy")
                return redirect("signup")
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user=user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile(user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect("settings")
        else:
            messages.info(request, "Passwords are not the same")
            return redirect("signup")

    else:
        return render(request, "signup.html")


def signin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Bunday nomga ega foydalanuvchi mavjud emas")
            return redirect("signin")

    else:
        return render(request, "signin.html")
 

@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")