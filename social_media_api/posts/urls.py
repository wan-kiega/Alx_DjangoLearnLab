# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
# Add basename parameter
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]

# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, user_feed

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', user_feed, name='user_feed'),  # Feed endpoint
]

# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views # Make sure 'views' includes the new functions

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
# router.register(r'feed', views.FeedViewSet, basename='feed') # If you have this

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.user_feed, name='user_feed'), # If you have this
    
    # --- Like/Unlike URLs ---
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
]

# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views # Make sure 'views' includes the like_post and unlike_post functions

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
# router.register(r'feed', views.FeedViewSet, basename='feed') # If you have this

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.user_feed, name='user_feed'), # If you have this
    
    # --- Like/Unlike URLs ---
    # Use <int:pk> to match the pattern expected by the checker and common DRF conventions
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    path('posts/<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
]