# api/views.py
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

# For Create, Update, and Delete, we typically require authentication
# We'll use CreateAPIView, UpdateAPIView, DestroyAPIView for single responsibility
# Or RetrieveUpdateDestroyAPIView for combined detail/update/delete

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    POST /api/books/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users

    def perform_create(self, serializer):
        # Hook to add logic before saving (e.g., set owner if your model has one)
        # serializer.save(owner=self.request.user)
        serializer.save() # Save the book instance


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    PUT /api/books/{id}/
    PATCH /api/books/{id}/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users

    def perform_update(self, serializer):
        # Hook to add logic before updating
        serializer.save() # Save the updated book instance


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    DELETE /api/books/{id}/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users

    def destroy(self, request, *args, **kwargs):
        # Optional: Customize the destroy response
        instance = self.get_object()
        # Example: Add a custom message before deletion
        title = getattr(instance, 'title', 'Unknown Book') # Safely get title
        self.perform_destroy(instance)
        return Response(
            {"message": f"Book '{title}' has been successfully deleted."},
            status=status.HTTP_204_NO_CONTENT
        )