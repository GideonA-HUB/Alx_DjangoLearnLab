import django
from django.conf import settings
from relationship_app.models import Author, Book, Library, Librarian

# Set up Django environment (if running this outside of the Django shell)
settings.configure(DEBUG=True)
django.setup()

# Sample Queries

# 1. Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = author.books.all()
    for book in books:
        print(f"Book Title: {book.title}")

# 2. List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    for book in books:
        print(f"Book Title: {book.title}")

# 3. Retrieve the librarian for a library
def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = library.librarian
    print(f"Librarian for {library.name}: {librarian.name}")

# Example usage:
# Replace these values with actual data in your database to test the queries
books_by_author('J.K. Rowling')
books_in_library('Central Library')
librarian_of_library('Central Library')
