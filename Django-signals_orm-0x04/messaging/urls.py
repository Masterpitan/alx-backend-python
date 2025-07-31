from django.urls import path
from .views import delete_user, unread_messages_view

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('unread/', unread_messages_view, name='unread_messages'),
]
