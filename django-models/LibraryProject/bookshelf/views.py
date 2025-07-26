from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from bookshelf.models import Book

def list_books(request):
    """
    Function-based view that lists all books and their authors
    """
    # Get all books with their authors
    books = Book.objects.select_related('author').all()
    
    # Pass books to template
    context = {
        'books': books
    }
    
    return render(request, 'relationship_app/book_list.html', context)