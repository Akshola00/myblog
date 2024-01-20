
from django.urls import path
from . import views
urlpatterns = [
    path("", views.homepage , name="about-page"),
    path("about/", views.aboutpage , name="about-page"),
    path("signup/", views.signup , name="signup-page"),
]