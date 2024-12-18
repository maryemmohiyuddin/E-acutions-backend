# notifications/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import create_notification
from .models import Notification
from rest_framework.permissions import AllowAny

class CreateNotificationView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request, *args, **kwargs):
        # Get the data from the request
        flag = request.data.get('flag')
        productname = request.data.get('productname')
        username = request.data.get('username')
        price = request.data.get('price')
        user_id = request.data.get('user_id')

        # Check for missing required fields
        if not all([flag, productname, username, price, user_id]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Call the utility function to create the notification
        create_notification(flag, productname, username, price, user_id)

        return Response({"message": "Notification created successfully!"}, status=status.HTTP_201_CREATED)
class GetNotificationsView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def get(self, request, *args, **kwargs):
        # Get unread notifications for the logged-in user
        notifications = Notification.objects.filter(user=request.user, status='unread')

        # Prepare data to return
        notification_data = [
            {"notification": notification.notification}
            for notification in notifications
        ]

        return Response({"notifications": notification_data}, status=status.HTTP_200_OK)
    
class MarkAsReadView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request, *args, **kwargs):
        # Get the list of notification IDs from the request
        notification_ids = request.data.get('notification_ids', [])

        if not notification_ids:
            return Response({"error": "No notification IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Try to bulk update the notifications to "read"
        notifications = Notification.objects.filter(id__in=notification_ids)
        if not notifications.exists():
            return Response({"error": "Some notifications not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the status of all notifications in the list to "read"
        notifications.update(status='read')

        return Response({"message": f"{notifications.count()} notifications marked as read"}, status=status.HTTP_200_OK)