from rest_framework import serializers
from .models import Author, Book
from datetime import date

# Serializer for the Book model.
# Serializes all fields of the Book model and validates publication year.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model.

    # Custom validation to ensure publication_year is not in the future.
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for the Author model.
# Includes the author's name and a nested list of related books.
class AuthorSerializer(serializers.ModelSerializer):
    # The books field uses BookSerializer to serialize related Book instances.
    # The 'books' data is read-only because it's generated dynamically from the relationship.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']  # Only return the author's name and their related books.

# Relationship Handling in Serializers:
# - The Book model has a ForeignKey to Author, establishing a One-to-Many relationship.
# - The 'related_name="books"' in the Book model lets AuthorSerializer fetch books as author.books.all().
# - AuthorSerializer uses a nested BookSerializer to return each author's books as a structured list.

# api/serializers.py (example additions)
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # Or list your fields explicitly

    def validate_publication_year(self, value):
        """Ensure publication year is not in the future."""
        from datetime import datetime
        if value and value > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    def validate(self, data):
        """Object-level validation (e.g., check relationships)."""
        # Example: Ensure title and author combination is unique
        # title = data.get('title')
        # author = data.get('author')
        # if title and author and Book.objects.filter(title=title, author=author).exists():
        #     raise serializers.ValidationError("A book with this title and author already exists.")
        return data
