from django.urls import path
from .views import CreateGroupChatAPIView, ChatsListAPIView, CreatePersonalChatAPIView, ChatDetailAPIView, UpdateGroupChatAPIView, GroupChatSearchAPIView, ChatDeleteAPIView, JoinToGroupChatAPIView


urlpatterns = [
    path('create-group-chat/', CreateGroupChatAPIView.as_view(), name='api-create-group-chat'),
    path('update-group-chat/<int:pk>/', UpdateGroupChatAPIView.as_view(), name='api-update-group-chat'),
    path('chats-list/', ChatsListAPIView.as_view(), name='api-chats-list'),
    path('create-personal-chat/', CreatePersonalChatAPIView.as_view(), name='api-create-personal-chat'),
    path('detail-chat/<int:pk>/', ChatDetailAPIView.as_view(), name='api-detail-chat'),
    path('search-group-chat/', GroupChatSearchAPIView.as_view(), name='api-search-group-chat'),
    path('delete-chat/<int:pk>/', ChatDeleteAPIView.as_view(), name='api-delete-chat'),
    path('join-to-group-chat/', JoinToGroupChatAPIView.as_view(), name='api-join-to-group-chat'),
]
