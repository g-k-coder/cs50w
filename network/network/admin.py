from django.contrib import admin
from .models import User, Post, Follow, Like

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'uuid')
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'time')
    
@admin.register(Follow)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follower')

@admin.register(Like)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user')
