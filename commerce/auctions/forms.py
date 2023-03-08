from django.forms import ModelForm
from django import forms


from .models import User, AuctionListing, Comment, Bid, CATEGORIES, Watchlist


class CreateListing(ModelForm):
    category = forms.ChoiceField(choices=CATEGORIES, required=True)
    picture = forms.ImageField(required=False)
    title = forms.CharField(required=True, widget=forms.TextInput(attrs = {
                                                                  'class': 'line', 
                                                                  'autocomplete': 'off', 
                                                                  'placeholder': "Title"
                                                                  }))
    price = forms.DecimalField(required=True, widget=forms.NumberInput(attrs = {
                                                                      'class': 'line',
                                                                      'step': 0.01,
                                                                      'min': 0,
                                                                      'placeholder': "Price in USD($)",
                                                                      'name': 'price'
                                                                      }))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs = {
                                                        'class': 'line',
                                                        'cols': '25', 
                                                        'rows': '10', 
                                                        'name': 'description',
                                                        'placeholder': 'Enter description of your listing'
                                                        }))
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=True)
    sold_to = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=True)

    closed = forms.IntegerField(required=True, widget=forms.HiddenInput(attrs = {'value': 0}))
    
    class Meta(ModelForm):
        model = AuctionListing
        fields = ['category', 'title', 'price', 'description', 'picture', 'user', 'sold_to', 'closed']
        
class PlaceBid(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=True)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all(), widget=forms.HiddenInput(), required=True)
    bid = forms.DecimalField(label='')
    
    class Meta(ModelForm):
        model = Bid
        fields = ['user', 'listing', 'bid']
        widget= { 'bid' : forms.NumberInput(attrs = {
                                            'name': 'bid'
                                            })}
        
class AddComment(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=True)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all(), widget=forms.HiddenInput(), required=True)
    comment = forms.CharField(label="", widget=forms.Textarea())
    
    class Meta(ModelForm):
        model = Comment
        fields = ['comment', 'listing', 'user']

class AddToWatchlist(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=True)
    listing = forms.ModelChoiceField(queryset=AuctionListing.objects.all(), widget=forms.HiddenInput(), required=True)
    
    class Meta(ModelForm):
        model = Watchlist 
        fields = ['user', 'listing']

        