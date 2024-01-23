import datetime

from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
	return render(request, 'index.html', {} )

def edit_profile(request):
	currently_user = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		name = request.POST['name']
		username = request.POST['username']
		location = request.POST['location']
		dob = request.POST['dob']
		# email = request.POST['email']
		website = request.POST['Website']
		bio = request.POST['bio']
		
		dob_ed = datetime.strptime(dob, "%m/%d/%Y")
		currently_user.full_name = name
		currently_user.username = username
		print('dob')
		print(dob)
		
		print('dob_ed')
		print(dob_ed)
		currently_user.location = location
		currently_user.dob = dob_ed
		currently_user.profile_img = currently_user.profile_img
		currently_user.bio = bio
		
		currently_user.website = website
		Profile.save()

	context = {
		'currently_user':currently_user
	}
	return render(request,"edit_profile.html", context)


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

from django.contrib.auth import authenticate, login, logout

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
