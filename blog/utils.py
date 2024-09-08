from django.contrib.auth.models import User
from .models import Profile, FollowRelationship

def get_current_user_profile(request):
    user = User.objects.get(username=request.user)
    return Profile.objects.get(user=user)

def get_user_profile(username):
    user = User.objects.get(username=username)
    return Profile.objects.get(user=user)

def get_people_to_follow(current_profile):
    user_following = FollowRelationship.objects.filter(follower=current_profile)
    following_profile_ids = [user.following.pk for user in user_following]
    all_profiles = Profile.objects.exclude(user=current_profile.user).exclude(pk__in=following_profile_ids)
    return list(all_profiles[:5])
