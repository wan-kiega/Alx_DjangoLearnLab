from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUser(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    username = forms.CharField(max_length=30, required=True)

class meta: 
    model = User
    fields = ("username", "email", "first_name", "last_name", "password")

def save (self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data["email"]
    user.first_name = self.cleaned_data.get("first_name", "")
    user.last_name = self.cleaned_data.get("last_name", "")
    if commit: 
        user.save()
    return user