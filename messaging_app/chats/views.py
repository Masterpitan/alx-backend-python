from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, CreateMessageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_403_FORBIDDEN

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']  # Filter by user ID in participants

    def get_queryset(self):
        return self.request.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if not participants or len(participants) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'conversation'] # Allow filtering messages by conversation ID
    filterset_class = MessageFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMessageSerializer
        return MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise Response(
                {"detail": "You are not a participant of this conversation."},
                status=HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get("conversation")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        message = serializer.save(sender=request.user, conversation=conversation)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
