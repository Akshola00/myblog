from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile
from django.contrib.auth import login, authenticate

# Create your views here.
def homepage(request):
	return render(request, 'index.html', {} )
	# return render(request, "")

def aboutpage(request):
	return HttpResponse("<h2> this is the about page</h2>")

def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		
		if User.objects.filter(email = email).exists():
			messages.warning( request, 'Email has Already Been Used🧐')
			return redirect("signup-page")
		elif User.objects.filter(username = username):
			messages.warning(request, "Username Taken😞")
			return redirect("signup-page")
		else:
			user_created = User.objects.create_user(username=username, password=password, email=email)
			
			user_created.save()
			currently_created_user = User.objects.get(username=username)
			profile_user = Profile.objects.create(user= currently_created_user)
			profile_user.save()
			return redirect("signin-page")
		
	return render(request, 'signup.html')

def signin(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		print(email)
		print(password)
		
		user = authenticate(request, user=email, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Succesfully Logged in🙂")
			return redirect("home-page")
		else:
			messages.warning(request, "Incorrect Email or Password, Try Again😕")
			return redirect('signin-page')
		

	return render(request, 'signin.html')

def edit_profile(request):
	return render(request,"edit_profile.html", {})