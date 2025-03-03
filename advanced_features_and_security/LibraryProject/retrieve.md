# Retrieve Operation

Command:
```python
# Retrieve all books
books = Book.objects.all()
for book in books:
    print(book)

# Expected output:
'1984' by George Orwell (1949)