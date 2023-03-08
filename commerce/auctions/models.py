from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Member since")
    picture = models.ImageField(default='default_avatar.png')

# https://docs.djangoproject.com/en/4.1/ref/models/fields/#choices
#! 'choices' must be an iterable containing (actual value, human readable name) tuples
    
CATEGORIES = [
    # Terse representation of the category, full name of the category 
    (None, 'Choose a category'),
    ('Arts & Crafts, DIY', 'Arts & Crafts, DIY'),
    ('Automotive & Industrial', 'Automotive & Industrial'),
    ('Baby & Child Care', 'Baby & Child Care'),
    ('Beauty & Personal Care', 'Beauty & Personal Care'),
    ('Books & Office Supplies', 'Books & Office Supplies'),
    ('Electronics & Technology', 'Electronics & Technology'),
    ('Fashion & Clothing', 'Fashion & Clothing'),
    ('Fiction & Magic', 'Fiction & Magic'),
    ('Food & Beverage', 'Food & Beverage'),
    ('Garden & Outdoor Living', 'Garden & Outdoor Living'),
    ('Health & Wellness', 'Health & Wellness'),
    ('Home & Kitchen', 'Home & Kitchen'),
    ('Music & Entertainment', 'Music & Entertainment'),
    ('Pet Supplies', 'Pet Supplies'),
    ('Sports & Outdoors', 'Sports & Outdoors'),
    ('Toys & Games', 'Toys & Games'),
    ('Other', 'Other')
]


class AuctionListing(models.Model):    
    category = models.CharField(max_length=50, choices=CATEGORIES, verbose_name="category")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", verbose_name="seller")
    picture = models.ImageField(default='default_listing.png')
    title = models.CharField(max_length=100, verbose_name='Title')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price in USD($)", validators=[MinValueValidator(0.01)])
    description = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Listed on")
    sold_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", verbose_name="buyer", null=True, blank=True)
    closed = models.IntegerField(max_length = 1, default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    def __str__(self):
        return f"@{self.user.username} listed \"{self.title}\""



class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", verbose_name="bidder")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_bid", verbose_name="Listing")
    bid = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Bid($)")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.listing.user.username} bid {self.bid}$ on {self.listing.title}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment", verbose_name="comment")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comment", verbose_name="Listing")
    comment = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.listing.user.username} commented on {self.listing.title} at {self.date}."


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching", verbose_name="Watching")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watch_listing", verbose_name="Listing")
    
    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"