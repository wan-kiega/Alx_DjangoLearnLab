# books/models.py
from django.db import models

# Author Model
# This model stores information about book authors
class Author(models.Model):
    # Store the author's name (required field)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        # Show author name when printing the object
        return self.name
    
    class Meta:
        # Sort authors alphabetically by name
        ordering = ['name']

# Book Model
# This model stores information about books
# Each book is connected to one author (many books can have the same author)
class Book(models.Model):
    # Store the book title (required field)
    title = models.CharField(max_length=200)
    
    # Store the publication year (required field)
    publication_year = models.IntegerField()
    
    # Connect each book to one author
    # One author can write many books (one-to-many relationship)
    # When an author is deleted, all their books are also deleted
    # related_name='books' allows us to get all books by an author using author.books.all()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        # Show book title and year when printing the object
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        # Sort books alphabetically by title
        ordering = ['title']