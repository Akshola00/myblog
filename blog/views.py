import datetime
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile, Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        d_user = User.objects.get(username=request.user)
        c_user_profile = Profile.objects.get(user=d_user)
        posts = Post.objects.all()
        context = {"post": posts, "c_user_profile": c_user_profile}
        return render(request, "index.html", context)
    else:
        return redirect("signin-page")
@login_required(login_url="signin-page")
def like_post(request):
    # getting the post
    post_id = request.GET.get("post_id")
    post_obj = Post.objects.get(id=post_id)

    # getting the user
    d_user = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=d_user)

    like_filter = Post.objects.filter(id=post_id, likes=user_profile).first()
    # likepostdb.objects.filter(post=post_obj, user=user_profile).first().delete()
    if like_filter is None:
        post_obj.likes.add(user_profile)
        return redirect("/")

    else:
        post_obj.likes.remove(user_profile)
        return redirect("/")


@login_required(login_url="signin-page")
def post(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        topic = request.POST.get("topic")
        caption = request.POST.get("caption")
        category = request.POST.get("category")
        d_user = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=d_user)
        newPost = Post.objects.create(
            user=user_profile, image=image, topic=topic, caption=caption
        )
        newPost.save()
        messages.success(request, "Post Uploaded Successfully")
        return redirect("home-page")

    context = {}
    return render(request, "upload_post.html", context)


@login_required(login_url="signin-page")
def userprofile(request, pk):

    d_user = User.objects.get(username=request.user)
    c_user_profile = Profile.objects.get(user=d_user)    
    d_user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=d_user)
    context = {"d_user": d_user, "user_profile": user_profile, 'c_user_profile': c_user_profile}
    return render(request, "profile_page.html", context)


# edit profile view
@login_required(login_url="signin-page")
def edit_profile(request):
    user_object = User.objects.get(username=request.user)
    currently_user = Profile.objects.get(user=user_object)

    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        location = request.POST.get("location")
        dob_str = request.POST.get("dob", "")
        website = request.POST.get("Website")
        bio = request.POST["bio"]

        # check if username has already been used

        # Update User fields
        user_object.first_name = name
        user_object.username = username
        user_object.save()

        # Update Profile fields
        currently_user.location = location
        currently_user.dob = dob_str
        currently_user.profile_img = currently_user.profile_img
        currently_user.bio = bio
        currently_user.website = website
        currently_user.save()
        messages.success(request, "Profile Info Successfully Edited🙂")
        return redirect("home-page")

    context = {"currently_user": currently_user}
    return render(request, "edit_profile.html", context)


# useless for now
@login_required(login_url="signin-page")
def edit_profile_img(request):
    return render(request, "edit_profile.html")


# signin view
def signin(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home-page')
            messages.success(request, "Successfully Logged in🙂")
            return redirect(next_url)
        else:
            messages.warning(request, "Incorrect Email or Password, Try Again😕")
            return redirect("signin-page")
    return render(request, "signin.html")

# signup view
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email has Already Been Used🧐")
            return redirect("signup-page")
        elif User.objects.filter(username=username).exists():
            messages.warning(request, "Username Taken😞")
            return redirect("signup-page")
        else:
            User.objects.create_user(username=username, password=password, email=email)
            currently_created_user = User.objects.get(username=username)
            profile_user = Profile.objects.create(user=currently_created_user)
            profile_user.save()
            return redirect("signin-page")

    return render(request, "signup.html")


# logout view
@login_required(login_url="signin-page")
def userlogout(request):
    logout(request)
    messages.success(request, "Successfully Logged out🥲")
    return redirect("home-page")
