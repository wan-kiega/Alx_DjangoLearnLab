from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library



def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"  
    context_object_name = "library"  



from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")  # Redirect to your existing book list view
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})



from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return render(request, "relationship_app/logout.html")



from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})




##Continuation

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")



##Last part

from django.contrib.auth.decorators import permission_required

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    return render(request, "relationship_app/add_book.html")

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    return render(request, "relationship_app/edit_book.html", {"book_id": book_id})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    return render(request, "relationship_app/delete_book.html", {"book_id": book_id})



##Trying

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .models import Book

@permission_required('relationship_app.can_add_book')
def add_book(request):
    return HttpResponse("Add book view - requires can_add_book permission")

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Edit book view for {book.title} - requires can_change_book permission")

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Delete book view for {book.title} - requires can_delete_book permission")

#updated
# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import Book, Library, UserProfile

# Your existing views
def list_books(request):
    """Function-based view that lists all books and their authors"""
    books = Book.objects.select_related('author').all()
    
    if books.exists():
        book_lines = []
        for book in books:
            author_name = book.author.name if book.author else "Unknown Author"
            book_lines.append(f"{book.title} by {author_name}")
        
        content = "Books List:\n" + "="*30 + "\n"
        content += "\n".join(book_lines)
        return HttpResponse(content, content_type='text/plain')
    else:
        return HttpResponse("No books available in the database.")

class LibraryDetailView(DetailView):
    """Class-based view that displays details for a specific library"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context

# Role checking functions
def is_admin(user):
    try:
        return user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False

def is_librarian(user):
    try:
        return user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False

def is_member(user):
    try:
        return user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users"""
    users = User.objects.all()
    user_profiles = UserProfile.objects.all()
    
    context = {
        'users': users,
        'user_profiles': user_profiles,
        'total_users': users.count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users"""
    libraries = Library.objects.all()
    books = Book.objects.all()
    
    context = {
        'libraries': libraries,
        'books': books,
        'total_libraries': libraries.count(),
        'total_books': books.count(),
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member)
def member_view(request):
    """View accessible only to Member users"""
    books = Book.objects.all()
    libraries = Library.objects.all()
    
    context = {
        'books': books,
        'libraries': libraries,
        'available_books': books.count(),
    }
    return render(request, 'relationship_app/member_view.html', context)

#create user
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Auto-login after registration
            login(request, user)
            messages.success(request, 'User created successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'register.html')

