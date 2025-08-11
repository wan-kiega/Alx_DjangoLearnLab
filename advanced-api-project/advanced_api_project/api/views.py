# api/views.py (Enhanced version)
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with filtering and search capabilities
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Automatically set the creator (if you have a creator field)
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    #Alternative
    # api/views.py (Alternative approach using ViewSets)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet providing complete CRUD operations for Book model:
    - list: GET /api/books/ - List all books
    - create: POST /api/books/ - Create new book
    - retrieve: GET /api/books/{id}/ - Get specific book
    - update: PUT /api/books/{id}/ - Update entire book
    - partial_update: PATCH /api/books/{id}/ - Partial update
    - destroy: DELETE /api/books/{id}/ - Delete book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']
    
    # Custom action example
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get books published in the last 5 years"""
        from datetime import datetime
        five_years_ago = datetime.now().year - 5
        recent_books = Book.objects.filter(publication_year__gte=five_years_ago)
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author model with nested books
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    #Updated version
    # api/views.py (Using custom permissions)
from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    Get all books - READ ONLY (Everyone can access)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Or IsAdminOrReadOnly for admin-write only

class BookDetailView(generics.RetrieveAPIView):
    """
    Get one book by ID - READ ONLY (Everyone can access)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    Create a new book - Only authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book - Only authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Or IsOwnerOrReadOnly

class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book - Only authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Or IsAdminOrReadOnly