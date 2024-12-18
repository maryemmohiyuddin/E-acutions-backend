# notifications/urls.py
from django.urls import path
from .views import CreateNotificationView
from .views import GetNotificationsView, MarkAsReadView

urlpatterns = [
    path('create-notification/', CreateNotificationView.as_view(), name='create-notification'),
    path('notifications/', GetNotificationsView.as_view(), name='notification-list'),
    path('notifications/mark-as-read/', MarkAsReadView.as_view(), name='mark-notifications-as-read'),

]
