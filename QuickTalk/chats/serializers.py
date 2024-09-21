from rest_framework import serializers
from .models import Chat
from django.utils.translation import gettext_lazy as _


class CreateGroupChatSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Chat
        fields = ['name', 'type', 'created_by', 'created_at']

    def create(self, validated_data):
        request_user = self.context['request'].user  # Получаем текущего пользователя из контекста запроса
        chat = Chat.objects.create(
            type='group',  # Мы явно указываем, что это групповой чат
            created_by=request_user,
            name=validated_data.get('name'),
        )
        
        # Добавляем создателя в список пользователей чата
        chat.users.add(request_user)
        return chat
    

class ChatsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'type']
        
