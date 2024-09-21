from django.urls import path
from .views import CreateGroupChatAPIView, ChatsListAPIView


urlpatterns = [
    path('create-group-chat/', CreateGroupChatAPIView.as_view(), name='api-create-group-chat'),
    path('chats-list/', ChatsListAPIView.as_view(), name='api-chats-list'),
]
