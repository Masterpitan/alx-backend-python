from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')

def get_conversation_thread(user):
    messages = Message.objects.filter(
        parent_message__isnull=True,
        receiver=user
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )
    return messages
