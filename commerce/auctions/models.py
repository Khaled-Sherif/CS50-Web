from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'Myapp'

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    watchlist = models.ManyToManyField('Listing', related_name="saved_listings_towatch")

    
    #email = models.EmailField(max_length=254, unique=True, db_index=True, primary_key=True)
    
    def __str__(self):
        return f"{self.email}\n{self.username}"

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    item_name = models.CharField(max_length=50, null=False)
    current_price = models.IntegerField(default=0)
    img = models.URLField(blank=True)
    category = models.CharField(max_length=50,
                                choices=(
                                        ("Electronics", "Electronics"),
                                        ("Fashion", "Fashion"),
                                        ("Motors", "Motors"),
                                        ("Sports", "Sports"),
                                        ("Art", "Art"),
                                        ("Furniture", "Furniture"),
                                        ("Collectibles", "Collectibles"),
                                    )
                                )
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction', blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.category} {self.date} {self.active}"
    
"""class Watchlist(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist')
    listings = models.ManyToManyField(Listing, related_name="listing_to_watch")

    def __str__(self):
        return f"{self.user} {self.listings}"""
    
class Bid(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='auction', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} {self.amount} {self.date}"
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='auctions')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user_id}: {self.comment}"