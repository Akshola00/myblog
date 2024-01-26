import datetime
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
	return render(request, 'index.html', {} )

def userprofile(request, pk):
    d_user = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = d_user)
    context = {
        "d_user" : d_user,
        "user_profile" : user_profile
    }
    return  render(request, "profile_page.html", context)
#edit profile view
def edit_profile(request):
    user_object = User.objects.get(username=request.user)
    currently_user = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        name = request.POST.get('name')
        print(name)
        username = request.POST.get('username')
        location = request.POST.get('location')
        dob_str = request.POST.get('dob', '')
        website = request.POST.get('Website')
        bio = request.POST['bio']

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

    context = {
        'currently_user': currently_user
    }
    return render(request, "edit_profile.html", context)

def edit_profile_img(request):
	return render(request,"edit_profile.html")

#signin view
def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in🙂")
            return redirect("home-page")
        else:
            messages.warning(request, "Incorrect Email or Password, Try Again😕")
            return render(request, 'signin-page')
	
    return render(request, 'signin.html')

#signup view
def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		
		if User.objects.filter(email = email).exists():
			messages.warning( request, 'Email has Already Been Used🧐')
			return redirect("signup-page")
		elif User.objects.filter(username=username).exists():
			messages.warning(request, "Username Taken😞")
			return redirect("signup-page")
		else:
			User.objects.create_user(username=username, password=password, email=email)
			currently_created_user = User.objects.get(username=username)
			profile_user = Profile.objects.create(user= currently_created_user)
			profile_user.save()
			return redirect("signin-page")
		
	return render(request, 'signup.html')

#logout view
@login_required(login_url='signin-page')
def userlogout(request):
	logout(request)
	messages.success(request, "Successfully Logged out🥲")
	return redirect("home-page")
