from bookshelf.models import Author, Book, Library, Librarian

# Author book query
author = Author.objects.get("specific author")
Book.objects.filter(author)

# Library books query
library = Library.objects.get(name="library_name")
library.books.all()
["Library.objects.get(name=library_name)" , "books.all()"]

# Librarian query
librarian = Librarian.objects.get(name = "specific librarian")
librarian.library



