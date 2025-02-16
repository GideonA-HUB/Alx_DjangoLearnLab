# Delete Operation

**Command**:
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
books = Book.objects.all()
print(books)

<QuerySet []>  # Empty queryset, since the book was deleted
