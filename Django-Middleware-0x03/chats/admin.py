from django.contrib import admin
from .models import User, Conversation, Message

#Registering my models
admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)
