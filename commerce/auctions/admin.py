from django.contrib import admin
from .models import AbstractUser
from .models import *

class ListingAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('watchlist',)

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)




