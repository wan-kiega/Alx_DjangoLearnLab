from bookshelf.models import Book
Book.objects.all().delete()

<!-- (1, {'bookshelf.Book': 1}) -->