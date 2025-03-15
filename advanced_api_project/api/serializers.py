from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serialization of books

    class Meta:
        model = Author
        fields = ['name', 'books']

 """
    Serializes data for the Book model.
    Includes a custom validation to ensure that the publication year is not in the future.
"""

 """
    Validates that the publication year is not in the future.
"""

 """
    Serializes data for the Author model.
    Includes a nested BookSerializer to serialize related books.
"""