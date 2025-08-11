from django.db import models

# The Author model represents a writer in the system.
# Each Author can be linked to multiple Book records (One-to-Many relationship).
class Author(models.Model):
    name = models.CharField(max_length=255)  # Stores the author's name.

    def __str__(self):
        return self.name  # Display the author's name in admin and shell.
    

# The Book model represents a published book in the system.
# Each Book is linked to one Author through a ForeignKey.
class Book(models.Model):
    title = models.CharField(max_length=255)  # Title of the book.
    publication_year = models.IntegerField()  # Year the book was published.
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,     # If an Author is deleted, their books are also deleted.
        related_name='books'          # Allows reverse access: author.books.all()
    )

    def __str__(self):
        return self.title  # Display the book title in admin and shell.
