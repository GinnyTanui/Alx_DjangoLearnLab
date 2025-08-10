from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Create an author
        self.author = Author.objects.create(name="Test Author")
        
        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2020
        )
        
        # Endpoints
        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book.id}/"

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2023
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "Should Fail",
            "author": self.author.id,
            "publication_year": 2023
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        self.client.login(username="testuser", password="testpass")
        data = {"title": "Updated Book"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

