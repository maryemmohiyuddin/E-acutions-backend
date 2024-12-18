# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]

    notification = models.TextField()  # The notification message
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # Foreign key to the User model
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='unread',  # Default to unread
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when created

    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification[:30]}..."  # Show first 30 chars for preview

    class Meta:
        ordering = ['-created_at']  # Order notifications by the most recent
