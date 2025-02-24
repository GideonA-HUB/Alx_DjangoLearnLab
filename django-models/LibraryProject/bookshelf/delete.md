# Delete Operation

**Command**:
```python
from bookshelf.models import Book  # This line imports the Book model

# Get the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Verify if the book was deleted
books = Book.objects.all()
print(books)

# Expected output:
<QuerySet []>  # Empty queryset, since the book was deleted
