
from django.urls import path
from . import views
urlpatterns = [
    path("", views.homepage , name="home-page"),
    path("about/", views.aboutpage , name="about-page"),


    path("signup/", views.signup , name="signup-page"),

    path("signin/", views.signin , name="signin-page"),
    path("edit_profile/", views.edit_profile , name="edit_profile-page"),

    path("logout/", views.userlogout, name="logout-page")
]