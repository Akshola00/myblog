
from django.urls import path
from . import views
urlpatterns = [
    path("", views.homepage , name="home-page"),
    # path("about/", views.aboutpage , name="about-page"),


    path("signup/", views.signup, name="signup-page"),

    path("signin/", views.signin, name="signin-page"),
    path("edit_profile/", views.edit_profile , name="edit_profile-page"),

    path("profile/<str:pk>/", views.userprofile , name="profile-page"),

    path("edit_profile_img", views.edit_profile_img , name="edit_profile_img-page"),

    path("logout", views.userlogout, name="logout-page"), 
    path("like_post", views.like_post, name="like_post"), 
    # path("changeimage", views.changeimage, name="changeimage"), 

    path("post_details/<str:pk>", views.post_details, name="post_details"),     

    path('liked_post/', views.liked_post, name='liked_post'),
    path('process_data/', views.process_data, name='process_data'),
    path('count_likes/', views.count_likes, name='count_likes'),
    path('check_liked/', views.check_liked, name='check_liked'),
    path('check_follow/', views.check_follow, name='check_follow'),
    path('saveabout/', views.saveabout, name='saveabout'),

    
    path("post", views.post, name="post-page"),
    path("search", views.search, name="search-page")
]