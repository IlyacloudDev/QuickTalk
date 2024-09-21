from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateGroupChatSerializer, ChatsListSerializer
from .models import Chat


class CreateGroupChatAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут создавать чаты

    def post(self, request, *args, **kwargs):
        serializer = CreateGroupChatSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            chat = serializer.save()  # Создание чата
            return Response({'detail': 'Group chat created successfully!', 'chat_id': CreateGroupChatSerializer(chat).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        chats = Chat.objects.filter(users=user)
        serializer = ChatsListSerializer(chats, many=True)
        return Response(serializer.data)
