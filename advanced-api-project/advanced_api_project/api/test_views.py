from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Book
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')  # Added login
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2020
        }
        self.book = Book.objects.create(**self.book_data)

    def test_list_books_unauthenticated(self):
        self.client.logout()  # Remove authentication
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_books_authenticated(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_books_by_author(self):
        response = self.client.get(reverse('book-list'), {'author': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Test Author')

    def test_filter_books_by_publication_year(self):
        response = self.client.get(reverse('book-list'), {'publication_year': 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2020)

    def test_search_books_by_title(self):
        response = self.client.get(reverse('book-list'), {'search': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_search_books_by_author(self):
        response = self.client.get(reverse('book-list'), {'search': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Test Author')

    def test_order_books_by_title(self):
        Book.objects.create(title='Another Book', author='Another Author', publication_year=2021)
        response = self.client.get(reverse('book-list'), {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Another Book')

    def test_order_books_by_publication_year_desc(self):
        Book.objects.create(title='Another Book', author='Another Author', publication_year=2021)
        response = self.client.get(reverse('book-list'), {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)

    def test_retrieve_book_unauthenticated(self):
        self.client.logout()  # Remove authentication
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_retrieve_book_authenticated(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_create_book_authenticated(self):
        new_book = {'title': 'New Book', 'author': 'New Author', 'publication_year': 2022}
        response = self.client.post(reverse('book-create'), new_book, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_create_book_unauthenticated(self):
        self.client.logout()  # Remove authentication
        response = self.client.post(reverse('book-create'), self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        update_data = {'id': self.book.pk, 'title': 'Updated Book', 'author': 'Test Author', 'publication_year': 2020}
        response = self.client.put(reverse('book-update'), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_update_book_empty_title(self):
        update_data = {'id': self.book.pk, 'title': '', 'author': 'Test Author', 'publication_year': 2020}
        response = self.client.put(reverse('book-update'), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_update_book_no_id(self):
        update_data = {'title': 'Updated Book', 'author': 'Test Author', 'publication_year': 2020}
        response = self.client.put(reverse('book-update'), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('id', response.data)

    def test_update_book_unauthenticated(self):
        self.client.logout()  # Remove authentication
        update_data = {'id': self.book.pk, 'title': 'Updated Book', 'author': 'Test Author', 'publication_year': 2020}
        response = self.client.put(reverse('book-update'), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        delete_data = {'id': self.book.pk}
        response = self.client.delete(reverse('book-delete'), delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_delete_book_no_id(self):
        response = self.client.delete(reverse('book-delete'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('id', response.data)

    def test_delete_book_unauthenticated(self):
        self.client.logout()  # Remove authentication
        delete_data = {'id': self.book.pk}
        response = self.client.delete(reverse('book-delete'), delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        