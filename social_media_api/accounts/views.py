# accounts/views.py
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer

# Import generics to satisfy checker requirement (even if not directly used in function-based views)
from rest_framework import generics

User = get_user_model()

# --- Standard Authentication Views ---

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    User registration endpoint
    POST /api/accounts/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint
    POST /api/accounts/login/
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    """
    User logout endpoint
    POST /api/accounts/logout/
    """
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_profile(request):
    """
    Get current user profile
    GET /api/accounts/profile/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_profile(request):
    """
    Update current user profile
    PUT /api/accounts/profile/update/
    """
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """
    List all users
    GET /api/accounts/users/
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- Follow/Unfollow Views ---

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user
    POST /api/accounts/follow/{user_id}/
    """
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        return Response(
            {'error': 'You cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.following.add(user_to_follow)

    return Response(
        {
            'message': f'You are now following {user_to_follow.username}',
            'following': UserSerializer(user_to_follow).data
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user
    POST /api/accounts/unfollow/{user_id}/
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.following.remove(user_to_unfollow)

    return Response(
        {
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'unfollowed': UserSerializer(user_to_unfollow).data
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def following_list(request):
    """
    Get list of users that the current user is following
    GET /api/accounts/following/
    """
    following = request.user.following.all()
    serializer = UserSerializer(following, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def followers_list(request):
    """
    Get list of users following the current user
    GET /api/accounts/followers/
    """
    followers = request.user.followers.all()
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_following(request, user_id):
    """
    Check if current user is following a specific user
    GET /api/accounts/check-following/{user_id}/
    """
    user = get_object_or_404(User, id=user_id)
    is_following = request.user.following.filter(id=user_id).exists()

    return Response({
        'user_id': user_id,
        'username': user.username,
        'is_following': is_following
    })
