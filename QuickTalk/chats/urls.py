from django.urls import path
from .views import CreateGroupChatAPIView, ChatsListAPIView, CreatePersonalChatAPIView


urlpatterns = [
    path('create-group-chat/', CreateGroupChatAPIView.as_view(), name='api-create-group-chat'),
    path('chats-list/', ChatsListAPIView.as_view(), name='api-chats-list'),
    path('create-personal-chat', CreatePersonalChatAPIView.as_view(), name='api-create-personal-chat'),
]
