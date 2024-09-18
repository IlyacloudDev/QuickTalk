from django.urls import path
from .views import CreateGroupChatAPIView


urlpatterns = [
    path('create-group-chat/', CreateGroupChatAPIView.as_view(), name='api-create-group-chat'),
]
