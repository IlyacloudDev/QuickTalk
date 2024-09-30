from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateGroupChatSerializer, ChatsListSerializer, CreatePersonalChatSerializer, ChatDeleteSerializer
from .models import Chat


class CreateGroupChatAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут создавать чаты

    def post(self, request, *args, **kwargs):
        serializer = CreateGroupChatSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            chat = serializer.save()  # Создание чата
            return Response({'detail': _('Group chat created successfully!'), 'chat_id': CreateGroupChatSerializer(chat).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateGroupChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": _("Method PUT not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = Chat.objects.get(pk=pk)
            if instance.type != 'group':
                return  Response({"error": _("Method PUT not allowed for personal chat")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            elif instance.created_by != request.user:
                return  Response({"error": _("Method PUT not allowed to non-chat creator")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Chat.DoesNotExist:
            return Response({"error": _("Object does not exist")}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateGroupChatSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePersonalChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Создаем экземпляр сериализатора с данными из запроса
        serializer = CreatePersonalChatSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            chat = serializer.save()
            return Response({
                'detail': _('Chat created successfully'),
                'chat_id': CreatePersonalChatSerializer(chat).data
            }, status=status.HTTP_201_CREATED)
        
        # Если валидация не прошла, отправляем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        chats = Chat.objects.filter(users=user).order_by('-created_at')
        serializer = ChatsListSerializer(chats, many=True, context={'request': request})
        return Response(serializer.data)
    

class ChatDetailAPIView(APIView):
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
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
             return Response({"error": _("Method DELETE not allowed")},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            chat = Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatDeleteSerializer()
        serializer.destroy(chat)

        return Response({"detail": _("Chat deleted successfully")}, status=status.HTTP_204_NO_CONTENT)
