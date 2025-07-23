from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or obj.user == request.user or obj.sender == request.user
