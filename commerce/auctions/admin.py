from django.contrib import admin

from .models import User, AuctionListing, Bid, Comment

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date')
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'date')

class ListingsAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date')
    list_display = ('id', 'category', 'user', 'title', 'price', 'date')

class BiddingsAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'date')
    list_display = ('id', 'listing', 'user', 'bid', 'date')
    
class CommentsAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'date')
    list_display = ('id', 'listing', 'user', 'comment', 'date')

admin.site.register(Comment, CommentsAdmin)
admin.site.register(AuctionListing, ListingsAdmin)
admin.site.register(Bid, BiddingsAdmin)
admin.site.register(User, UsersAdmin)