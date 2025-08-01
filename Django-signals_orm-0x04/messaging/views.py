from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Message
from django.views.decorators.cache import cache_page

@cache_page(60)
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
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')  # Optional for threaded replies

        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return render(request, 'messaging/send_message.html', {'error': 'Receiver not found.'})

        parent = None
        if parent_id:
            try:
                parent = Message.objects.get(pk=parent_id)
            except Message.DoesNotExist:
                pass  # Ignore invalid parent

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent
        )
        return HttpResponseRedirect(reverse('inbox'))

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/send_message.html', {'users': users})

def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/unread_messages.html', {'messages': unread_messages})
