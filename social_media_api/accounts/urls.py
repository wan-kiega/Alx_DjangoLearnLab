# accounts/urls.py
from django.urls import path
from . import views

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Registration endpoint - returns token upon successful registration
    path('register/', views.register, name='register'),
    
    # Login endpoint - returns token upon successful login
    path('login/', views.login_view, name='login'),
    
    # User profile management endpoints
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]