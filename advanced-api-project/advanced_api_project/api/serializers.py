# books/serializers.py
from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

# BookSerializer
# This serializer converts Book model data to JSON and vice versa
# It handles all fields of the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields: title, publication_year, author
    
    # Custom validation to make sure publication year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            # Stop the request if year is in the future
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer
# This serializer converts Author model data to JSON
# It includes the author's name and all their books (nested serialization)
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer: shows all books written by this author
    # many=True because one author can have many books
    # read_only=True because we don't want to create books when creating an author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        # Only include the name field and the nested books
        fields = ['name', 'books']

# How the relationship works:
# 1. In the models: Book has a ForeignKey to Author with related_name='books'
# 2. In the serializers: AuthorSerializer includes 'books' which uses BookSerializer
# 3. This creates a nested structure where each author shows their related books
# Example output:
# {
#   "name": "George Orwell",
#   "books": [
#     {"title": "1984", "publication_year": 1949, "author": 1},
#     {"title": "Animal Farm", "publication_year": 1945, "author": 1}
#   ]
# }