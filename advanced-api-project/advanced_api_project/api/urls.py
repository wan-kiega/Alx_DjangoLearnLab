# books/urls.py
from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    # List all books
    path('', BookListView.as_view(), name='book_list'),
    
    # Show one book
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    
    # Create new book
    path('book/new/', BookCreateView.as_view(), name='book_create'),
    
    # Update existing book
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    
    # Delete book
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]

#Alternative option
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookListView, BookDetailView, BookCreateView, 
    BookUpdateView, BookDeleteView, BookViewSet
)

urlpatterns = [
    # Book CRUD operations
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]