from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create listing"),
    path("categories", views.categories, name='categories'),
    path("watchlist", views.watchlist, name='watchlist'),
    path("categories/<category>", views.categories, name='categories'),
    path("listing/<int:list_id>", views.view_listing, name='view listing'),
    path("listing/<int:list_id>/add_comment", views.add_comment, name='add comment'),
    path("listing/<int:list_id>/place_bid", views.place_bid, name='place bid'),
    path("listing/<int:list_id>/close_auction", views.close_auction, name='close auction'),
    path("listing/<int:list_id>/edit_watchlist", views.edit_watchlist, name='edit_watchlist')
]

