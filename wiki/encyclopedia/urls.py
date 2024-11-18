from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create-new-page/", views.create_new_page, name="new-page"),
    path("wiki/save-new-article", views.save_new_article, name="save-new-article"),
    path("wiki/edit-content/", views.edit_content, name="edit_content"),
    path("wiki/edit-content/<str:entry>", views.edit_content, name="edit_content"),
    path("wiki/search/", views.searchresults, name="search"),
    path("wiki/rndm-artcl/", views.random_page, name="random_page"),
    path("wiki/<str:entry>/", views.page, name="page"),
    path("wiki/<str:entry>/edit-content", views.edit_content, name="edit_content"),
]
