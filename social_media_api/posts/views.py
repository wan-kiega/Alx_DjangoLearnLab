# posts/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
from django.contrib.contenttypes.models import ContentType
from .models import Like
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from notifications.models import Notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# posts/views.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework.generics import get_object_or_404

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """
    Get posts from users that the current user follows, ordered by creation date (newest first)
    GET /api/posts/feed/
    """
    # Get posts from users that the current user follows
    following_users = request.user.following.all()
    feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Apply pagination if you have it configured
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    try:
        page_size = int(page_size)
        if page_size > 100:  # Limit page size
            page_size = 100
    except (ValueError, TypeError):
        page_size = 10
    
    # Manual pagination
    start = (int(page) - 1) * page_size
    end = start + page_size
    paginated_posts = feed_posts[start:end]
    
    # Serialize the posts
    serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
    
    return Response({
        'count': feed_posts.count(),
        'page': int(page),
        'page_size': page_size,
        'results': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    """
    Like a post.
    POST /api/posts/{post_id}/like/
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({'message': 'You have already liked this post.'}, status=status.HTTP_200_OK)
    else:
        # --- Create Notification ---
        # Use the helper method from the Notification model
        Notification.create_notification(
            recipient=post.author, # The post owner receives the notification
            actor=request.user,    # The user who liked the post
            verb='liked your post', # The action description
            target=post            # The post that was liked
        )
        # --- End Create Notification ---

        return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
    

# Alternative ViewSet approach
class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for user feed - posts from followed users
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get posts from users that the current user follows
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

# Keep your existing ViewSets...
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Ensure user is authenticated
def like_post(request, post_id):
    """
    Like a post.
    POST /api/posts/{post_id}/like/
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        # --- Generate Notification ---
        # Check if notification logic is in a separate app/service
        # Example using a hypothetical Notification model in 'notifications' app:
        try:
            # Import here to avoid potential circular import issues if notifications depends on posts
            from notifications.models import Notification
            # Avoid notifying a user for liking their own post
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,      # The post owner receives the notification
                    actor=request.user,         # The user who liked the post
                    verb='liked',               # The action
                    target=post,                # The post that was liked
                )
        except ImportError:
            # Handle case where notifications app/model might not be available
            # or log an error/warning
            print("Warning: Notifications app/model not found for like action.")
            pass # Silently fail notification creation if app is missing
        
        return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Ensure user is authenticated
def unlike_post(request, post_id):
    """
    Unlike a post.
    POST /api/posts/{post_id}/unlike/
    """
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    # --- Remove the like ---
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        
        # --- Optional: Delete corresponding notification ---
        # This part depends on how you want to manage notifications.
        # You might choose to keep them for history, or remove them.
        # Example of removing the notification:
        try:
            from notifications.models import Notification
            # Find the specific notification for this like action
            # This assumes the structure created in like_post
            notification_content_type = ContentType.objects.get_for_model(post)
            Notification.objects.filter(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target_content_type=notification_content_type,
                target_object_id=post.id
            ).delete() # Delete the specific notification
            # Note: Be careful with bulk deletes if other 'like' notifications exist.
            # A more robust approach might involve linking the Notification directly to the Like instance.
            
        except ImportError:
             print("Warning: Notifications app/model not found for unlike action.")
             pass
            
        return Response({'message': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'error': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
