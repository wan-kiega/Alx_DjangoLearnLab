from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import NotFound
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from .models import Book
from .serializers import BookSerializer
from rest_framework import serializers

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter, rest_filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        book_id = self.request.data.get('id')
        if not book_id:
            raise serializers.ValidationError({"id": "Book ID is required in the request body."})
        try:
            return self.queryset.get(pk=book_id)
        except Book.DoesNotExist:
            raise NotFound("Book not found.")

    def perform_update(self, serializer):
        if not serializer.validated_data.get('title'):
            raise serializers.ValidationError({"title": "Title cannot be empty."})
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        book_id = self.request.data.get('id')
        if not book_id:
            raise serializers.ValidationError({"id": "Book ID is required in the request body."})
        try:
            return self.queryset.get(pk=book_id)
        except Book.DoesNotExist:
            raise NotFound("Book not found.")