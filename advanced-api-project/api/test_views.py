from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):
    
    def setUp(self):
        # Setup code: create test users and books
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.book = Book.objects.create(title='Test Book', author='Test Author', price=29.99)

    def test_create_book(self):
        """Test creating a new book."""
        self.client.login(username='testuser', password='testpassword')
        data = {'title': 'New Book', 'author': 'New Author', 'price': 19.99}
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_read_book(self):
        """Test reading a book."""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book(self):
        """Test updating a book."""
        self.client.login(username='testuser', password='testpassword')
        data = {'title': 'Updated Book', 'author': 'Updated Author', 'price': 39.99}
        response = self.client.put(f'/api/books/{self.book.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        """Test deleting a book."""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        Book.objects.create(title='Another Book', author='Another Author', price=25.99)
        response = self.client.get('/api/books/?author=Test Author')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Test Author')

    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get('/api/books/?search=Test Book')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_order_books_by_price(self):
        """Test ordering books by price."""
        Book.objects.create(title='Cheap Book', author='Cheap Author', price=10.99)
        response = self.client.get('/api/books/?ordering=price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['price'] <= response.data[1]['price'])

    def test_permission_for_non_authenticated_user(self):
        """Test permissions for unauthenticated users."""
        response = self.client.post('/api/books/', {'title': 'No Permission', 'author': 'No Author', 'price': 9.99}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_for_admin_user(self):
        """Test permissions for admin users."""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
