from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library



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





