# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class Notification(models.Model):
    """
    Model to store notifications for users.
    """
    # The user who receives the notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # The user who performed the action (e.g., liked the post, commented)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions' # e.g., actor.actions.all()
    )

    # A verb describing the action (e.g., "liked", "commented on", "started following")
    verb = models.CharField(max_length=255)

    # --- Generic Foreign Key to link to different types of objects (Post, Comment, etc.) ---
    # The type of the target object (e.g., Post, Comment)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # The ID of the target object
    target_object_id = models.PositiveIntegerField()
    # The actual target object (Post instance, Comment instance, etc.)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    # Timestamp of when the notification was created
    timestamp = models.DateTimeField(default=timezone.now)

    # Optional: Mark notification as read
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.recipient.username} <- {self.actor.username} {self.verb} {self.target} ({self.timestamp})"

    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.is_read:
            self.is_read = True
            self.save()

    def mark_as_unread(self):
        """Mark this notification as unread."""
        if self.is_read:
            self.is_read = False
            self.save()
# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class Notification(models.Model):
    """
    Model to store notifications for users.
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actor_notifications'
    )
    verb = models.CharField(max_length=255) # e.g., "liked", "commented on", "started following"

    # --- Generic Foreign Key ---
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True) # Allow null/blank for actions without a specific target object
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    # --- End Generic Foreign Key ---

    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        if self.target:
            return f"{self.recipient} <- {self.actor} {self.verb} {self.target} ({self.timestamp})"
        else:
            return f"{self.recipient} <- {self.actor} {self.verb} ({self.timestamp})"

    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    def mark_as_unread(self):
        """Mark this notification as unread."""
        if self.is_read:
            self.is_read = False
            self.save(update_fields=['is_read'])

    @classmethod
    def create_notification(cls, recipient, actor, verb, target=None):
        """
        Class method to create a notification.
        Handles ContentType association for the target object if provided.
        """
        if recipient == actor:
            # Optional: Don't notify users about their own actions
            return None

        notification_data = {
            'recipient': recipient,
            'actor': actor,
            'verb': verb,
        }
        if target:
            notification_data['target_content_type'] = ContentType.objects.get_for_model(target)
            notification_data['target_object_id'] = target.id

        return cls.objects.create(**notification_data)
