"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='start.html'), name='start'),
    path('login/', TemplateView.as_view(template_name='users/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='users/register.html'), name='register'),
    path('update-user/', TemplateView.as_view(template_name='users/update.html'), name='update-user'),
    path('logout/', TemplateView.as_view(template_name='users/logout.html'), name='logout'),
    path('search/', TemplateView.as_view(template_name='users/search.html'), name='search-user'),
    path('detail-user/', TemplateView.as_view(template_name='users/detail.html'), name='detail-user'),

    path('create-group-chat/', TemplateView.as_view(template_name='chats/create_group_chat.html'), name='create-group-chat'),
    path('chats-list/', TemplateView.as_view(template_name='chats/chats_list.html'), name='chats-list'),
    path('detail-chat/', TemplateView.as_view(template_name='chats/detail.html'), name='detail-chat'),

    path('api/users/', include('users.urls')),
    path('api/chats/', include('chats.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
