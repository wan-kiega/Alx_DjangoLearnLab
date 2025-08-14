from django.shortcuts import render, redirect
from .forms import CustomUser

# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else: form = CustomUser()
        return render(request, "/register.html", {"form": form})