from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

# profile table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_img =  models.ImageField( upload_to='profile_images', default='default.jpg')
    location = models.CharField(null=True, blank=True, max_length=100)
    website = models.CharField(null=True, blank=True,max_length=100)
    # user_liked_posts = models.ForeignKey(Post, on_delete= models.SET_NULL, null= True)
    about = models.TextField(null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    def __str__(self):
        return self.user.username


class category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category
    
      
class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    user = models.ForeignKey(Profile, on_delete= models.SET_NULL, null= True)
    image = models.ImageField(upload_to='post_images', default=None, null=True, blank=True)
    topic = models.CharField(max_length=100, null = True, blank=True)
    caption = models.TextField()
    category = models.ManyToManyField(category, related_name='cats', blank=True)
    created = models.DateTimeField(default = datetime.now)
    likes = models.ManyToManyField(Profile, related_name='likes', blank=True)
    # comments = 
    def __str__(self):
        return self.caption
    
class Message(models.Model):
    muser = models.ForeignKey(Profile, on_delete= models.SET_NULL, null= True)
    mpost = models.ForeignKey(Post, on_delete= models.SET_NULL, null= True)
    message_body = models.TextField()
    created = models.DateTimeField(default = datetime.now)
    # likes =
    def __str__(self):
        return self.message_body
    


class FollowRelationship(models.Model):
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following_user')
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"