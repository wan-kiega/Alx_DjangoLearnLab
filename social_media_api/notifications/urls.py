from django.urls import path
from . import views

urlpatterns = [
    # --- Function-Based View URLs ---
    path('', views.user_notifications, name='user_notifications'),
    path('<int:notification_id>/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark-all-as-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    
]
