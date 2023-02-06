from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Member since")
    picture = models.ImageField(upload_to='auctions/static/auctions/profile/', default='auctions/profile/default_avatar.png')



class AuctionListing(models.Model):    
    
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#choices
    #! 'choices' must be an iterable containing (actual value, human readable name) tuples
    
    CATEGORIES = [
        # Terse representation of the category, full name of the category 
        ('DIY', 'Arts & Crafts, DIY'),
        ('Industrial', 'Automotive & Industrial'),
        ('Baby', 'Baby & Child Care'),
        ('Care', 'Beauty & Personal Care'),
        ('Office', 'Books & Office Supplies'),
        ('Tech', 'Electronics & Technology'),
        ('Fashion', 'Fashion & Clothing'),
        ('Magic', 'Fiction & Magic'),
        ('Food', 'Food & Beverage'),
        ('Garden', 'Garden & Outdoor Living'),
        ('Health', 'Health & Wellness'),
        ('Home', 'Home & Kitchen'),
        ('Music', 'Music & Entertainment'),
        ('Pet', 'Pet Supplies'),
        ('Sports', 'Sports & Outdoors'),
        ('Games', 'Toys & Games'),
        ('Other', 'Other')
    ]
    
    
    category = models.CharField(max_length=10, choices=CATEGORIES, verbose_name="category")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", verbose_name="seller")
    picture = models.ImageField(upload_to='auctions/static/auctions/listing/', default='auctions/listing/default_listing.png')
    title = models.CharField(max_length=100, verbose_name='Title')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Starting bid($)", validators=[MinValueValidator(0.01)])
    description = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Listed on")
    
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
