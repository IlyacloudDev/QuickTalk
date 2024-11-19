from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='start.html'), name='start'),
    path('login/', TemplateView.as_view(template_name='users/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='users/register.html'), name='register'),
    path('update-user/', TemplateView.as_view(template_name='users/update.html'), name='update-user'),
    path('logout/', TemplateView.as_view(template_name='users/logout.html'), name='logout'),
    path('search/', TemplateView.as_view(template_name='users/search.html'), name='search-user'),
    path('detail-user/', TemplateView.as_view(template_name='users/detail.html'), name='detail-user'),

    path('create-group-chat/', TemplateView.as_view(template_name='chats/create_group_chat.html'), name='create-group-chat'),
    path('update-group-chat/', TemplateView.as_view(template_name='chats/update_group_chat.html'), name='update-group-chat'),
    path('chats-list/', TemplateView.as_view(template_name='chats/chats_list.html'), name='chats-list'),
    path('search-group-chat/', TemplateView.as_view(template_name='chats/search_group_chat.html'), name='search-group-chat'),
    path('detail-chat/', TemplateView.as_view(template_name='chats/detail.html'), name='detail-chat'),
    path('delete-chat/', TemplateView.as_view(template_name='chats/delete.html'), name='delete-chat'),
    path('detail-group-chat/', TemplateView.as_view(template_name='chats/grp-cht-dtl-from-search.html'), name='detail-group-chat'),
]
