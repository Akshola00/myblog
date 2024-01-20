from django.db import models
from django.contrib.auth.models import User


# profile table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_img =  models.ImageField( upload_to='profile_images', default='default.jpg')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username