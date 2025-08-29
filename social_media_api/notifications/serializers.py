# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Simple serializer for user details in notifications."""
    class Meta:
        model = User
        fields = ['id', 'username']

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for the Notification model."""
    actor = UserSerializer(read_only=True) # Show actor details
    # target will be serialized as a generic representation or ID/name if needed
    # You might want to customize how the target is represented based on its type
    # For simplicity, we can show the target's string representation if it exists
    target_str = serializers.SerializerMethodField() # Custom field for target representation

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_str', 'timestamp', 'is_read']
        read_only_fields = ['id', 'actor', 'verb', 'target_str', 'timestamp', 'is_read']

    def get_target_str(self, obj):
        """Get a string representation of the target object."""
        if obj.target:
            # You could customize this further, e.g., return a link or specific fields
            return str(obj.target)
        return None
