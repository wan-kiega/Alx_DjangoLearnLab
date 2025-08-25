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

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    
    # Follow/Unfollow endpoints
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('following/', views.following_list, name='following_list'),
    path('followers/', views.followers_list, name='followers_list'),
    path('check-following/<int:user_id>/', views.check_following, name='check_following'),
]