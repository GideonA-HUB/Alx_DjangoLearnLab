# LibraryProject/bookshelf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Book list page
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('example/', views.example_view, name='example_form'), 
]
