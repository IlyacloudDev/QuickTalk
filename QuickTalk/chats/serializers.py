from rest_framework import serializers
from .models import Chat
from users.models import CustomUser
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
    

class CreatePersonalChatSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    chosen_user_to_prsnl_cht_id = serializers.IntegerField(write_only=True)  # Это поле только для записи

    class Meta:
        model = Chat
        fields = ['name', 'type', 'created_by', 'created_at', 'chosen_user_to_prsnl_cht_id']  # Убираем это поле после создания

    def validate(self, data):
        # Проверка на наличие существующего чата
        request_user = self.context['request'].user
        other_user = CustomUser.objects.get(pk = data['chosen_user_to_prsnl_cht_id'])
        
        existing_chat = Chat.objects.filter(
            type='personal',
            users=request_user
        ).filter(users=other_user).exists()

        if existing_chat:
            raise serializers.ValidationError("A personal chat between these users already exists.")
        return data

    def create(self, validated_data):
        request_user = self.context['request'].user
        other_user_id = validated_data.pop('chosen_user_to_prsnl_cht_id')  # Убираем из данных для модели
        other_user = CustomUser.objects.get(pk=other_user_id)
        chat = Chat.objects.create(
            type='personal',
            created_by=request_user,
        )
        # Добавляем обоих пользователей в чат
        chat.users.add(request_user, other_user)
        return chat


class ChatsListSerializer(serializers.ModelSerializer):
    chat_name = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['chat_name', 'type']  # 'chat_name' вместо 'name'

    def get_chat_name(self, obj):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        return obj.get_chat_name(user)  # Используем метод модели для получения имени или номера телефона
