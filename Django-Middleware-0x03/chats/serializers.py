from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_email = serializers.SerializerMethodField()

    def get_sender_email(self, obj):
        return obj.sender.email if obj.sender else None

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_email', 'message_body', 'sent_at', 'conversation']
        read_only_fields = ['message_id', 'sent_at', 'sender']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at']


# Custom validator to trigger serializers.ValidationError
class CreateMessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    class Meta:
        model = Message
        fields = ['message_body', 'conversation']
