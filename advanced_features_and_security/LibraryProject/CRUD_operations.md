# Create Operation

**Command**:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)

# Expected output:
'1984' by George Orwell (1949)

# Retrieve Operation

Command:
```python
# Retrieve all books
books = Book.objects.all()
for book in books:
    print(book)

# Expected output:
'1984' by George Orwell (1949)

# Update Operation

**Command**:
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)

# Expected output:
'Nineteen Eighty-Four' by George Orwell (1949)

# Delete Operation

**Command**:
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
books = Book.objects.all()
print(books)

<QuerySet []>  # Empty queryset, since the book was deleted
