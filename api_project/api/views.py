from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # Query to retrieve all books
    serializer_class = BookSerializer  # Serializer to convert Book model instances to JSON