# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Add custom fields to the user detail view
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture', 'followers')
        }),
    )
    
    # Add custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture')
        }),
    )
    
    list_display = UserAdmin.list_display + ('bio', 'followers_count', 'following_count')

# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)