from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):

    def setUp(self):
        """Setup test data"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.book1 = Book.objects.create(title="Book One", author="Author One", publication_year=2000)
        self.book2 = Book.objects.create(title="Book Two", author="Author Two", publication_year=2010)

        self.book_list_url = reverse("book-list")  # URL for listing and creating books

    def test_list_books(self):
        """Test retrieving the list of books"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        """Test that an authenticated user can create a book"""
        self.client.login(username="testuser", password="testpassword")
        data = {"title": "New Book", "author": "New Author", "publication_year": 2022}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Test that an unauthenticated user cannot create a book"""
        data = {"title": "Unauthorized Book", "author": "Unknown", "publication_year": 2023}
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_single_book(self):
        """Test retrieving a single book"""
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_update_book(self):
        """Test updating a book"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        updated_data = {"title": "Updated Title", "author": "Author One", "publication_year": 2005}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        """Test deleting a book"""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("book-detail", kwargs={"pk": self.book2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books(self):
        """Test filtering books by author"""
        response = self.client.get(self.book_list_url, {"author": "Author One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        """Test searching books by title"""
        response = self.client.get(self.book_list_url, {"search": "Book One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        """Test ordering books by publication year"""
        response = self.client.get(self.book_list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]["publication_year"] <= response.data[1]["publication_year"])
