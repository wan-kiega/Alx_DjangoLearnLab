from django.db import models

# Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
# Book Model
class Book(models.Model):
    title = models.CharField(max_length=1000)
    author = models.ForeignKey(Author, on_delete = models.PROTECT)
    
    def __str__(self):
        return f"{self.title} by {self}"

    
# Library Model
class Library(models.Model):
    name = models.CharField(max_length=1000)
    books = models.ManyToManyField(Book)
    
    def __str__(self):
        return self.name
    
# Librarian Model
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete = models.SET_NULL, null=True)
