from bookshelf.models import Book
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

<!-- <Book: 1984 (1949) by George Orwell> -->

from bookshelf.models import Book
Book.objects.all()

<!-- <QuerySet [<Book: 1984 (1949) by George Orwell>]> -->

from bookshelf.models import Book
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four" 
book.save()

<!-- <bound method Model.save of <Book: Nineteen Eighty-Four (1949) by George Orwell>> -->

from bookshelf.models import Book
Book.objects.all().delete()

<!-- (1, {'bookshelf.Book': 1}) -->