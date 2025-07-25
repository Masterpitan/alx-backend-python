from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or obj.user == request.user or obj.sender == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """For setting chat permissions"""
    def has_permissions(self, request, view):
        """Access for only authenticated Users"""
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        """For participants in conversation and access to
        both messages and objects"""
        user = request.user

        if hasattr(obj, 'participants'): # This is for conversations
            return user in obj.participants.all()

        # This is for message objects
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        else:
            return False
