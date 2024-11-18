from django.db.models import Max
from django import forms
from .models import Listing, Bid




def validate_bid_input(bid_amount, listing_id):
    bid_amount = bid_amount
    current_price = Listing.objects.filter(id=listing_id).first().current_price
    highest_bid = Bid.objects.filter(listing=listing_id).aggregate(Max('amount'))['amount__max']
    highest_bid = highest_bid  if highest_bid else 0
    
    if bid_amount <= highest_bid or bid_amount <= current_price:
        raise forms.ValidationError("Bid value should be more than the current price and highest Bid!")
    return True

    