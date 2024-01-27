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

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    user = models.ForeignKey(Profile, on_delete= models.SET_NULL, null= True)
    image = models.ImageField(upload_to='post_images', default=None, null=True)
    topic = models.CharField(max_length=100, null = True, blank=True)
    caption = models.TextField()
    created = models.DateTimeField(default = datetime.now)
    # likes = 
    # comments = 
    def __str__(self):
        return self.user.user.username