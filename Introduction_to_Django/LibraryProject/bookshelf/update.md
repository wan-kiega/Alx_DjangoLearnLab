from bookshelf.models import Book
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four" 
book.save()

<!-- <bound method Model.save of <Book: Nineteen Eighty-Four (1949) by George Orwell>> -->
