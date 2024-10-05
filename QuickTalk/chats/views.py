from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateGroupChatSerializer, ChatsListSerializer, CreatePersonalChatSerializer, ChatDeleteSerializer
from .models import Chat


class CreateGroupChatAPIView(APIView):
    """
    API View for creating a new group chat.

    Only authenticated users are allowed to create group chats. 
    The request must include the 'name' field. The chat creator is automatically 
    added to the chat members list.

    Methods:
        post(request): Creates a new group chat.

    Returns:
        Response: Details of the created chat or validation errors.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreateGroupChatSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            chat = serializer.save()
            return Response({'detail': _('Group chat created successfully.'), 'chat_id': CreateGroupChatSerializer(chat).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateGroupChatAPIView(APIView):
    """
    API View for updating an existing group chat.

    Only the creator of the group chat is allowed to update its details. 
    The method ensures that only group chats can be updated and validates 
    whether the user requesting the update is the chat creator.

    Methods:
        put(request, pk): Updates the group chat with the given ID (pk).

    Returns:
        Response: Updated chat data or appropriate error messages.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": _("Method PUT not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = Chat.objects.get(pk=pk)
            if instance.type != 'group':
                return Response({"error": _("Method PUT not allowed for personal chat")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            elif instance.created_by != request.user:
                return Response({"error": _("Method PUT not allowed to non-chat creator")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Chat.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateGroupChatSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePersonalChatAPIView(APIView):
    """
    API View for creating a new personal chat between two users.

    Users can create personal chats with other users. The system checks if a 
    personal chat between the two users already exists before creating a new one.

    Methods:
        post(request): Creates a new personal chat between the authenticated user and the chosen user.

    Returns:
        Response: Details of the created personal chat or validation errors.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreatePersonalChatSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            chat = serializer.save()
            return Response({
                'detail': _('Chat created successfully.'),
                'chat_id': CreatePersonalChatSerializer(chat).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatsListAPIView(APIView):
    """
    API View for listing all chats that the authenticated user is a part of.

    The chats are ordered by the date they were created in descending order.

    Methods:
        get(request): Retrieves the list of chats for the authenticated user.

    Returns:
        Response: List of chats the user is a part of.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        chats = Chat.objects.filter(users=user).order_by('-created_at')
        serializer = ChatsListSerializer(chats, many=True, context={'request': request})
        return Response(serializer.data)


class ChatDetailAPIView(APIView):
    """
    API View for retrieving the details of a specific chat.

    Allows authenticated users to get the details of a chat by its ID (pk). 
    Validates if the chat exists.

    Methods:
        get(request, pk): Retrieves chat details.

    Returns:
        Response: Chat details or error if the chat does not exist.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": _("Method GET not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = Chat.objects.get(pk=pk)
            instance_serializer = ChatsListSerializer(instance, context={'request': request}).data
        except Chat.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': instance_serializer})


class ChatDeleteAPIView(APIView):
    """
    API View for deleting a specific chat.

    Allows authenticated users to delete a chat by its ID (pk). 
    Validates if the chat exists before deletion.

    Methods:
        delete(request, pk): Deletes the chat.

    Returns:
        Response: Success message upon successful deletion or error message if the chat does not exist.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
             return Response({"error": _("Method DELETE not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            chat = Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatDeleteSerializer()
        serializer.destroy(chat)

        return Response({"detail": _("Chat deleted successfully.")}, status=status.HTTP_204_NO_CONTENT)
