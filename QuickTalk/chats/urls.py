from django.urls import path
from .views import CreateGroupChatAPIView, ChatsListAPIView, CreatePersonalChatAPIView, ChatDetailAPIView, UpdateGroupChatAPIView, ChatDeleteAPIView


urlpatterns = [
    path('create-group-chat/', CreateGroupChatAPIView.as_view(), name='api-create-group-chat'),
    path('update-group-chat/<int:pk>/', UpdateGroupChatAPIView.as_view(), name='api-update-group-chat'),
    path('chats-list/', ChatsListAPIView.as_view(), name='api-chats-list'),
    path('create-personal-chat/', CreatePersonalChatAPIView.as_view(), name='api-create-personal-chat'),
    path('detail-chat/<int:pk>/', ChatDetailAPIView.as_view(), name='api-detail-chat'),
    path('delete-chat/<int:pk>/', ChatDeleteAPIView.as_view(), name='api-delete-chat'),
]
