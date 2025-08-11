# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # Title of the blog post (up to 200 characters)
    title = models.CharField(max_length=200)
    
    # Content of the blog post (long text)
    content = models.TextField()
    
    # When the post was published (automatically set when created)
    published_date = models.DateTimeField(auto_now_add=True)
    
    # Author of the post (links to Django's built-in User model)
    # One author can write many posts (one-to-many relationship)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        # Show title when printing the object
        return self.title
    
    class Meta:
        # Sort posts by published date (newest first)
        ordering = ['-published_date']