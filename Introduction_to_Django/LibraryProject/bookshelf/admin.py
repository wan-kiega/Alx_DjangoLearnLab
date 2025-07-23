from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register

class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'publication_year')
  search_fields = ('title', 'author')
  list_filter = ('publication_year')

