import datetime
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Profile, Post, category as catdb, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        d_user = User.objects.get(username=request.user)
        c_user_profile = Profile.objects.get(user=d_user)
        posts = Post.objects.all()
        page = Paginator(posts, 3)
        pagelist = request.GET.get("page")
        page = page.get_page(pagelist)
        context = {"post": page, "c_user_profile": c_user_profile}

        return render(request, "index.html", context)
    else:
        return redirect("signin-page")


def search(request):
    q = request.GET.get("q")
    type = request.GET.get("type")
    d_user = User.objects.get(username=request.user)
    c_user_profile = Profile.objects.get(user=d_user)
    post = None
    people = None

    if type == "post":
        post = Post.objects.filter(Q(caption__icontains=q) | Q(topic__icontains=q))
    elif type == "category":
        post = Post.objects.filter(category__category__icontains=q)
    elif type == "people":
        people = Profile.objects.filter(
            Q(user__username__icontains=q) | Q(user__first_name__icontains=q)
        )
    else:
        # Handle invalid type
        pass

    context = {
        "post": post,
        "c_user_profile": c_user_profile,
        "searchterm": q,
        "people": people,
        "type": type,  # Pass type to template for UI handling
    }
    return render(request, "SearchPage.html", context)


@login_required(login_url="signin-page")
def like_post(request):
    # getting the post
    post_id = request.GET.get("post_id")
    post_obj = Post.objects.get(id=post_id)

    # getting the user
    d_user = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=d_user)

    like_filter = Post.objects.filter(id=post_id, likes=user_profile).first()
    previous_url = request.META.get("HTTP_REFERER")
    if like_filter is None:
        post_obj.likes.add(user_profile)
        return HttpResponseRedirect(previous_url)

    else:
        post_obj.likes.remove(user_profile)
        return HttpResponseRedirect(previous_url)




# def changeimage(request):
#     if request.method == "POST":
#         # Retrieve the uploaded image from the request.FILES attribute
#         thisimage = request.FILES.get("img")
#         print("Received image:", thisimage)  # Print the received image
        
#         # Save the image to the user's profile (if necessary)
#         # Your code to save the image goes here
        
#         return JsonResponse({'success': True})

#     # Return a failure response for unsupported request methods
#     return JsonResponse({'success': False, 'message': 'Unsupported request method.'}
#                         )
#     # Return a failure response for unsupported request methods
#     return JsonResponse({'success': False, 'message': 'Unsupported request method.'})
@login_required(login_url="signin-page")
def post_details(request, pk):
    d_user = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=d_user)
    c_user_profile = Profile.objects.get(user=d_user)
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all()
    if request.method == "POST":
        Message.objects.create(
            muser=user_profile, mpost=post, message_body=request.POST.get("messagebody")
        ).save()
        return redirect("post_details", pk=post.id)

    context = {
        "postdet": post,
        "c_user_profile": c_user_profile,
        "post_messages": post_messages,
    }
    return render(request, "postpage.html", context)


@login_required(login_url="signin-page")
def post(request):
    d_user = User.objects.get(username=request.user)
    c_user_profile = Profile.objects.get(user=d_user)
    all_cat = catdb.objects.all()
    if request.method == "POST":
        if request.FILES.get("file") != None:
            image = request.FILES.get("file")
        else:
            image = None
        topic = request.POST.get("topic")
        caption = request.POST.get("caption")
        n_ategory = request.POST.get("main_cats")
        newn = n_ategory.split()
        print(newn)

        d_user = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=d_user)

        newPost = Post.objects.create(
            user=user_profile,
            image=image,
            topic=topic,
            caption=caption,
        )

        # getting the category

        for x in newn:
            print(x)
            catdb.objects.get_or_create(category=x)
            dcat = catdb.objects.get(category=x)
            newPost.category.add(dcat)
        newPost.save()
        messages.success(request, "Post Uploaded Successfully")
        return redirect("home-page")

    context = {"all_cat": all_cat, "c_user_profile": c_user_profile}
    return render(request, "upload_post.html", context)


@login_required(login_url="signin-page")
def userprofile(request, pk):
    d_user = User.objects.get(username=request.user)
    c_user_profile = Profile.objects.get(user=d_user)

    d_user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=d_user)
    posts = user_profile.post_set.all()

    context = {
        "d_user": d_user,
        "user_profile": user_profile,
        "post": posts,
        "c_user_profile": c_user_profile,
    }
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
            next_url = request.GET.get("next", "home-page")
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
