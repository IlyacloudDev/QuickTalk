from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CreateGroupChatSerializer,
    ChatsListSerializer,
    CreatePersonalChatSerializer,
    ChatDeleteSerializer,
    JoinToGroupChatSerializer,
)
from .models import Chat


class CreateGroupChatAPIView(APIView):
    """
    Handles group chat creation by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreateGroupChatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            chat = serializer.save()
            return Response(
                {
                    'detail': _('Group chat created successfully.'),
                    'chat_id': CreateGroupChatSerializer(chat).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateGroupChatAPIView(APIView):
    """
    Allows group chat creators to update their chat details.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return Response({"error": _("Method PUT not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = Chat.objects.get(pk=pk)
            if instance.type != 'group':
                return Response({"error": _("Method PUT not allowed for personal chat")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            if instance.created_by != request.user:
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
    Enables users to create personal chats with others.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreatePersonalChatSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            chat = serializer.save()
            return Response(
                {
                    'detail': _('Chat created successfully.'),
                    'chat_id': CreatePersonalChatSerializer(chat).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatsListAPIView(APIView):
    """
    Retrieves a list of chats the authenticated user is part of.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(users=request.user).order_by('-created_at')
        serializer = ChatsListSerializer(chats, many=True, context={'request': request})
        return Response(serializer.data)


class ChatDetailAPIView(APIView):
    """
    Fetches details of a specific chat by its ID.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return Response({"error": _("Method GET not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = Chat.objects.get(pk=pk)
            instance_serializer = ChatsListSerializer(instance, context={'request': request}).data
        except Chat.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': instance_serializer})


class GroupChatSearchAPIView(APIView):
    """
    Searches group chats by name based on a substring query.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('query', '')
        group_chats = Chat.objects.filter(name__icontains=search_query, type="group") if search_query else Chat.objects.none()
        serializer = ChatsListSerializer(group_chats, many=True, context={'request': request})
        return Response(serializer.data)


class ChatDeleteAPIView(APIView):
    """
    Deletes a chat specified by its ID.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return Response({"error": _("Method DELETE not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            chat = Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatDeleteSerializer()
        serializer.destroy(chat)

        return Response({"detail": _("Chat deleted successfully.")}, status=status.HTTP_204_NO_CONTENT)


class JoinToGroupChatAPIView(APIView):
    """
    Adds a user to a specified group chat.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = JoinToGroupChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': _('The user was successfully added to the chat.')},
            status=status.HTTP_201_CREATED
        )
