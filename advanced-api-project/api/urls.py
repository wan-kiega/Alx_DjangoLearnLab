# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- Book CRUD URLs ---
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'), # Changed <int:pk>
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'), # Changed <int:pk>
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'), # Changed <int:pk>
]