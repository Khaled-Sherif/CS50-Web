from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import NumberInput
from django.db.models import Max
from .validators import validate_bid_input
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


 
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'img', 'category', 'current_price', 'description']
        
        
class RangeInput(NumberInput):
    input_type = 'range'
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
    def __init__(self, *args, **kwargs):
        self.listing_id = kwargs.pop('listing_id', None)
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        if self.request.method == "POST":
            cleaned_data = super().clean()
            bid_amount = cleaned_data['amount']
            validate_bid_input(bid_amount, self.listing_id)
            #print(f"\n\n{bid_amount}\n\n")
    
        
class WatchlistForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['watchlist']