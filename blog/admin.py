from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(category)
admin.site.register(Message)
admin.site.register(FollowRelationship)
admin.site.register(Like)
