from django.contrib import admin
from .models import Profile, Post, category, Message, FollowRelationship
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(category)
admin.site.register(Message)
admin.site.register(FollowRelationship)
