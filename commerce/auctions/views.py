from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateListing, PlaceBid, AddComment, AddToWatchlist

from .models import User, AuctionListing, Comment, Bid, CATEGORIES, Watchlist



# Void function, doesn't return anything just sets the prices up-to-date
def update_prices():
    for listing in AuctionListing.objects.all():
        try:
            new_price = Bid.objects.filter(listing_id=listing.pk).last()
            if new_price.bid > listing.price:
                AuctionListing.objects.filter(pk=listing.pk).update(price=new_price.bid)
        except AttributeError:
            continue
        
    return

def index(request):
    return render(request, "auctions/index.html", {
        "listings":  AuctionListing.objects.all()
    })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.", 
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.", 
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username,
                                            first_name=first_name, 
                                            last_name=last_name,  
                                            email=email, 
                                            password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.", 
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id, user_id=None):
    update_prices()
    listing = AuctionListing.objects.get(pk=listing_id)
    
    if not request.user.is_authenticated or user_id is None:
        return render(request, 'auctions/listing.html', {
        "listing": listing,
        "Num_bids": len(Bid.objects.all().filter(listing_id=listing.pk)),
        "comments": Comment.objects.all().filter(listing_id=listing.pk),
        "users": User.objects.all(),
        "current_bid": Bid.objects.all().filter(listing_id=listing.pk).last() 
    })
    
    watchlist_form = AddToWatchlist(request.POST or None, initial={'listing': listing_id, 'user': user_id}) 
    bid_form = PlaceBid(request.POST or None, initial={'listing': listing_id, 'user': user_id})
    bid_form.fields['bid'].widget.attrs.update({'min': listing.price+1, 'max': 9999.99, 'step': '0.01', 'placeholder': 'Bid'}) 
    comment_form = AddComment(request.POST or None, initial={'listing': listing_id, 'user': user_id}) 
    comment_form.fields['comment'].widget.attrs.update({'cols': 40, 'rows': 5, 'placeholder': 'Place your comment here'})
    
    
    if request.GET.get('close'):
        try:
            buyer = Bid.objects.filter(listing_id=listing.pk).last()
            listing.sold_to = buyer.user
        except AttributeError:
            pass
        
        listing.closed = 1
        listing.save()
        
        return render(request, 'auctions/listing.html', {
            "listing": listing,
            "comments": Comment.objects.all().filter(listing_id=listing.pk),
            "current_bid": Bid.objects.all().filter(listing_id=listing.pk).last()
        })
     
    
    watchlist = Watchlist.objects.filter(listing_id=listing_id).filter(user_id=user_id)
    
    if request.method == 'POST':
        
        # Initiate only the submitted forms
        if watchlist_form.is_valid():
            if len(watchlist) == 0:
                watchlist_form.save()
            else:
                Watchlist.objects.filter(listing_id=listing_id).filter(user_id=user_id).delete()
                
        if bid_form.is_valid():
            bid_form.save()
            
        if comment_form.is_valid():
            comment_form.save()
                
        
        return HttpResponseRedirect(f"/listing/{listing_id}/{user_id}")
    
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "Num_bids": len(Bid.objects.all().filter(listing_id=listing.pk)),
        "comments": Comment.objects.all().filter(listing_id=listing.pk),
        "users": User.objects.all(),
        "place_bid": bid_form,
        "add_comment": comment_form,
        "current_bid": Bid.objects.all().filter(listing_id=listing.pk).last(),
        "watchlist_form": watchlist_form,
        "check_watchlist": len(watchlist)
    })


@login_required
def create_listing(request, user_id):
    form = CreateListing(request.POST or None, request.FILES or None, initial={'user': user_id, 'sold_to': user_id, 'closed': 0})
    
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'auctions/create-listing.html', {
            "form": form,
            "user_id": user_id
        })    
    
    form.save()
    
    listing = AuctionListing.objects.filter(user_id=user_id).last()
    
    return HttpResponseRedirect(f"/listing/{listing.pk}/{user_id}")      
        
@login_required
def watchlist(request, user_id):
    return render(request, "auctions/watchlist.html", {
        "listings": Watchlist.objects.filter(user_id=user_id).only('listing') 
    })

@login_required
def user_listings(request, user_id):
    return render(request, "auctions/listings.html", {
        "listings": AuctionListing.objects.filter(user_id=user_id) 
    })

def category(request, category_name=None):
    if category_name is None:
        return render(request, "auctions/category.html", {
            "categories": CATEGORIES[1:], 
        })
    elif request.method == "POST":
        return HttpResponseRedirect(f"/category/{category_name}")
        
    listings = []
    
    for listing in AuctionListing.objects.filter(category=category_name):
        if not listing.closed:
            listings.append(listing)
    
    if not len(listings):
        return render(request, "auctions/category.html", { 
            "error": 'No listings in this category.',
            "category": category_name 
        })
    else:
        return render(request, "auctions/category.html", {
            "listings": listings,
            "category": category_name
        })