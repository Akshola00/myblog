from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def homepage(request):
	return render(request, 'index.html', {} )
	# return render(request, "")

def aboutpage(request):
	return HttpResponse("<h2> this is the about page</h2>")

def signup(request):
	return HttpResponse('this seems to be the dignup page')