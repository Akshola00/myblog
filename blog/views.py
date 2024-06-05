import datetime
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Profile, Post, category as catdb, Message, FollowRelationship, Like
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from itertools import chain


@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.profile
        # Check if the user has already liked the post
        if not Like.objects.filter(user=user_profile, post=post).exists():
            # If not, create a new like
            Like.objects.create(user=user_profile, post=post)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'You have already liked this post.'})
    else:
        return JsonResponse({'success': False, 'message': 'You must be logged in to like a post.'})


@csrf_exempt
def check_follow(request):
    if request.method == "POST":
        id = request.POST.get("username")
        print("abido shaker of them all ################     :     ", id)
        d_user = User.objects.get(id=id)
        up = Profile.objects.get(user=d_user)

        c_user = User.objects.get(username=request.user)
        c_user_profile = Profile.objects.get(user=c_user)

        # print("****************username = ", up.bio)
        # print("****************username = ", c_user_profile.bio)
        follow_relationship = FollowRelationship.objects.filter(follower=c_user_profile, following=up).first()
        if follow_relationship:
            return JsonResponse({ 'is_following': False })
        else:
            return JsonResponse({ 'is_following': True })


@csrf_exempt  # Disable CSRF protection for this view (for simplicity)

def process_data(request):
    if request.method == "POST":
        id = request.POST.get("username")

        print("Received username:", id)  # Print the received username to the console

        d_user = User.objects.get(id=id)
        up = Profile.objects.get(user=d_user)

        c_user = User.objects.get(username=request.user)
        c_user_profile = Profile.objects.get(user=c_user)

        # print("****************username = ", up.bio)
        # print("****************username = ", c_user_profile.bio)
        follow_relationship = FollowRelationship.objects.filter(follower=c_user_profile, following=up).first()

        if FollowRelationship.objects.filter(
            follower=c_user_profile, following=up
        ).exists():
            follow_relationship.delete()
        else:
            FollowRelationship.objects.create(follower=c_user_profile, following=up)

        return JsonResponse({"message": "Data received successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        user_following_list = []
        feed = []

        d_user = User.objects.get(username=request.user)
        c_user_profile = Profile.objects.get(user=d_user)
 
        posts = Post.objects.all().order_by('-created')
        page = Paginator(posts, 7)
        pagelist = request.GET.get("page")
        page = page.get_page(pagelist)

        #  to get the notificatrion posts
        user_following = FollowRelationship.objects.filter(follower=c_user_profile)
        # user_following = FollowRelationship.objects.filter(follower=c_user_profile)
        
        # num_following = FollowRelationship.objects.filter(follower=user_profile).count()
        for users in user_following:
            user_following_list.append(users.following)


        for username in user_following_list:
            # m_user_profile = Profile.objects.get(user=username)
            feed_list = Post.objects.filter(user=username).order_by('-created')
            feed.append(feed_list)

        feed_lists = list(chain(*feed))

        followers_profiles = c_user_profile.userfol.all()



        posts_by_followers = Post.objects.filter(user__in=followers_profiles)
        page = Paginator(feed_lists, 7)
        pagelist = request.GET.get("page")
        page = page.get_page(pagelist)

        # all__users = Profile.objects.all()
        user_following_all = []

        for user in user_following:
            user_list = Profile.objects.get(user=user.following.user)
            user_following_all.append(user_list)

        # new_suggestion_list = [x for x in list(all__users) if (x not in list(user_following_all))]
        # current_user = Profile.objects.filter(user=request.user)
        # final_suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
        
        following_profile_ids = [user.following.pk for user in user_following]  # Extract following profile IDs (changed)
        all_profiles = Profile.objects.exclude(user=request.user).exclude(pk__in=following_profile_ids)
        final_suggestion_list = list(all_profiles[:5])

        import random

        random.shuffle(final_suggestion_list)
        
        username_profile = []
        username_profile_list = []


        for users in final_suggestion_list:
            username_profile.append(users.id)

        for id in username_profile:
            profile_lists = Profile.objects.filter(id=id)
            username_profile_list.append(profile_lists)

        suggestions_username_profile_list = list(chain(*username_profile_list))

        context = {"post": page, "c_user_profile": c_user_profile, 'post_not':posts_by_followers, "suggestions_username_profile_list":suggestions_username_profile_list }

        return render(request, "index.html", context)
    else:
        return redirect("signin-page")

def notification(request):
    
    d_user = User.objects.get(username=request.user)
    c_user_profile = Profile.objects.get(user=d_user)

    followers_profiles = c_user_profile.userfol.all()

    posts_by_following = Post.objects.filter(user__in=followers_profiles)

    posts = c_user_profile.post_set.all()
    # Retrieve all the posts created by the user
    posts_by_user = c_user_profile.post_set.all()
    
    # List to store all comments
    all_comments = []
    all_likes = []
    
    # Loop through each post and extract associated comments
    for post in posts_by_user:
        comments = Message.objects.filter(mpost=post)
        likes = Like.objects.filter(post=post)
        all_likes.extend(likes)
        all_comments.extend(comments)
   

    context = {
        'c_user_profile':c_user_profile,
        'post':posts_by_following, 
        'post_messages':all_comments,
        'post_likes':all_likes,
        
    }
    return render(request, 'notifications.html', context)

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
#                        )
#     # Return a failure response for unsupported request methods
#     return JsonResponse({'success': False, 'message': 'Unsupported request method.'})
    

@login_required(login_url="signin-page")
def post_details(request, pk):
    d_user = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=d_user)
    c_user_profile = Profile.objects.get(user=d_user)
    post = Post.objects.get(id=pk)
    post_messages = post.message_set.all()
    post_likes = post.like_set.all()
    if request.method == "POST":
        Message.objects.create(
            muser=user_profile, mpost=post, message_body=request.POST.get("messagebody")
        ).save()
        return redirect("post_details", pk=post.id)

    context = {
        "postdet": post,
        "c_user_profile": c_user_profile,
        "post_messages": post_messages,
        "post_likes": post_likes,
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
        # print(newn)

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
            # print(x)
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

       
    md_user = User.objects.get(username=request.user) # getting the current use
    c_user_profile = Profile.objects.get(user=md_user)

    d_user = User.objects.get(username=pk) # what we are using 
    user_profile = Profile.objects.get(user=d_user)
    posts = user_profile.post_set.all()


# Assuming `profile` is an instance of the Profile model
# Find the number of followers for a specific profile
    num_followers = FollowRelationship.objects.filter(following=user_profile).count()

# Find the number of people the profile is following
    num_following = FollowRelationship.objects.filter(follower=user_profile).count()
    follow_relationship = FollowRelationship.objects.filter(follower=c_user_profile, following=user_profile).first()
    if follow_relationship:
        cs = 'Following'
    else:
        cs = 'Follow'


    context = {
        "d_user": d_user,
        "user_profile": user_profile,
        "post": posts,
        "c_user_profile": c_user_profile,
        'cs':cs,
        'num_followers':num_followers,
        'num_following':num_following
    }
    return render(request, "profile_page.html", context)

def saveabout(request):
    user_object = User.objects.get(username=request.user)
    currently_user = Profile.objects.get(user=user_object)
    abt = request.POST.get('about')
    print(abt)
    currently_user.about = abt
    currently_user.save()
    messages.success(request, "Profile Info Successfully Edited🙂")
    return redirect("profile-page", user_object)

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
