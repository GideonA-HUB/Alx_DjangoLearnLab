# LibraryProject/bookshelf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Book list page
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),  # Book detail page
]
