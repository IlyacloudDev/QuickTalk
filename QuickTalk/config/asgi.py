"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""


import os
import django
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Устанавливаем DJANGO_SETTINGS_MODULE до любого другого импорта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Явно инициализируем Django приложения
django.setup()


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chats.routing


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    ),
})
