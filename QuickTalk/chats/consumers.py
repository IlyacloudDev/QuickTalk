import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Присоединяемся к группе чата
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Принимаем соединение
        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы чата
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Получаем текущего пользователя из WebSocket соединения
        user = self.scope['user']

        # Получаем чат по его идентификатору
        try:
            chat = await self.get_chat(self.chat_id)
        except Chat.DoesNotExist:
            return

        # Создаем и сохраняем сообщение
        message = await self.create_message(chat, user, message_content)

        # Отправляем сообщение в группу чата
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'username': message.sender.username,  # Для отображения имени отправителя
                'user_id': message.sender.id,
                'timestamp': str(message.timestamp),  # Форматируем временную метку
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        user_id = event['user_id']
        timestamp = event['timestamp']

        # Отправляем сообщение обратно в WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'user_id': user_id,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def get_chat(self, chat_id):
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def create_message(self, chat, user, content):
        return Message.objects.create(chat=chat, sender=user, content=content)
