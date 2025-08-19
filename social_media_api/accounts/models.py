# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True, 
        help_text="Upload a profile picture"
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='following'
    )
    
    def __str__(self):
        return self.username
    
    # Add these methods that the admin is looking for
    def followers_count(self):
        """Returns the number of followers this user has"""
        return self.followers.count()
    
    def following_count(self):
        """Returns the number of users this user is following"""
        return self.following.count()
    
    # Make them display properly in admin
    followers_count.short_description = 'Followers'
    following_count.short_description = 'Following'