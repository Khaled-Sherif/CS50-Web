from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import *
from .helpers import in_watchlist


def index(request):
    listings = Listing.objects.all()
    if not listings:
        messages.info(request, "There are no auctions in the current time")
    return render(request, "auctions/index.html", {'listings': listings})


@login_required(login_url='/login')  
def create_listing(request):
    auction_form = ListingForm(request.POST)

    if request.method == "POST":
        if auction_form.is_valid():
            new_auction = auction_form.save(commit=False)
            new_auction.user = request.user
            new_auction.item_name = auction_form.cleaned_data['item_name']
            new_auction.img = auction_form.cleaned_data['img']
            new_auction.current_price = auction_form.cleaned_data['current_price']
            new_auction.category = auction_form.cleaned_data['category']
            
            new_auction.save()
        return HttpResponseRedirect(reverse('view listing', args=(new_auction.id,)))
    else:
        return render(request, "auctions/create listing.html", {'auction_form': auction_form})
                      
@login_required(login_url='/login')                    
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()    

    return render(request, "auctions/watchlist.html", {'watchlist':watchlist})

def categories(request, category=None):
    if  category:
        listings = Listing.objects.filter(category=category)
        if not listings:
            messages.info(request, "There are no auctions for this category in the current time")
        return render(request, "auctions/index.html", {'listings': listings})
    else:
        categories = Listing._meta.get_field('category').choices
        return render(request, "auctions/categories.html", {'categories': categories})
    
def view_listing(request, list_id):
    user = request.user
    listing = Listing.objects.get(id=list_id)
    bid_form = BidForm(listing_id=list_id, request=request)
    comment_form = CommentForm(request.POST)
    bids = Bid.objects.filter(id=list_id)
    highest_bid = Bid.objects.filter(listing=list_id).aggregate(Max('amount'))['amount__max']
    bids_count = Bid.objects.filter(listing=list_id).count()
    comments = Comment.objects.filter(listing=list_id)
    return render(request, "auctions/listingDetails.html", {'listing': listing,
                    'forms':{
                        'Bid': bid_form,
                        'Comment': comment_form},
                    'bids_info':{
                        "bids": bids,
                        "highest_bid": highest_bid,
                        "bids_count": bids_count,
                    },
                    "comments": comments,
                    "in_watchlist": in_watchlist(user, list_id)
                })
    
@login_required(login_url='/login')      
def add_comment(request, list_id):
    listing = Listing.objects.get(id=list_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.listing = listing
        new_comment.save()
    return HttpResponseRedirect(reverse('view listing', args=(listing.id,)))

@login_required(login_url='/login')  
def place_bid(request, list_id):
    listing = Listing.objects.get(id=list_id)
    bid_form = BidForm(request.POST, listing_id=list_id, request=request)
    if bid_form.is_valid():
        new_bid = bid_form.save(commit=False)
        new_bid.user = request.user
        new_bid.listing = listing
        new_bid.save()
        messages.success(request, "Bid has been successfully submitted!")
    else:
        messages.error(request, "Bid value should be more than the current price and highest Bid!")
    return HttpResponseRedirect(reverse('view listing', args=(listing.id,)))

def close_auction(request, list_id):
    listing = Listing.objects.get(id=list_id)
    if request.user == listing.user:
        winner = Bid.objects.filter(listing=list_id).order_by('-amount')[0].user
        listing.active = False
        listing.winner = winner
        listing.save()

    return HttpResponseRedirect(reverse('view listing', args=(listing.id,)))

@login_required(login_url='/login')  
def edit_watchlist(request, list_id):
    listing = Listing.objects.get(id=list_id)
    user = request.user
    
    if user.watchlist.filter(id=list_id).exists():
        user.watchlist.remove(listing)
        user.save()
    else:
        user.watchlist.add(listing)
        user.save()

    return HttpResponseRedirect(reverse('view listing', args=(listing.id,)))

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
                "message": "Invalid username and/or password."
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
