from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notification
from .serializers import NotificationSerializer 

# --- Function-Based View to List Notifications ---
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_notifications(request):
    """
    Get the current user's notifications.
    GET /api/notifications/
    Supports filtering for unread notifications.
    Query Parameters:
        - unread=true (to get only unread notifications)
    """
    user_notifications = request.user.notifications.all()

    # Filter for unread notifications if requested
    unread_filter = request.query_params.get('unread', '').lower()
    if unread_filter == 'true':
        user_notifications = user_notifications.filter(is_read=False)
        serializer = NotificationSerializer(user_notifications, many=True)
    return Response(serializer.data)

# --- Function-Based View to Mark Notifications as Read ---
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    """
    Mark a specific notification as read.
    POST /api/notifications/{notification_id}/mark-as-read/
    """
    try:
        notification = request.user.notifications.get(id=notification_id)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found or not yours.'}, status=status.HTTP_404_NOT_FOUND)

    notification.mark_as_read()
    return Response({'message': 'Notification marked as read.'}, status=status.HTTP_200_OK)


# --- Function-Based View to Mark All Notifications as Read ---
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_as_read(request):
    """
    Mark all of the current user's notifications as read.
    POST /api/notifications/mark-all-as-read/
    """
    unread_notifications = request.user.notifications.filter(is_read=False)
    updated_count = unread_notifications.update(is_read=True) # Bulk update is efficient
    return Response(
        {'message': f'{updated_count} notifications marked as read.'},
        status=status.HTTP_200_OK
    )