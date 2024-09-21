from django.urls import path
from .views import CustomUserLoginAPIView, CustomUserCreateAPIView, CustomUserLogoutAPIView, CustomUserUpdateAPIView, CustomUserSearchAPIView

urlpatterns = [
    path('login/', CustomUserLoginAPIView.as_view(), name='api-login'),
    path('register/', CustomUserCreateAPIView.as_view(), name='api-register'),
    path('logout/', CustomUserLogoutAPIView.as_view(), name='api-logout'),
    path('update-user/<int:pk>/', CustomUserUpdateAPIView.as_view(), name='api-update-user'),
    path('search-user/', CustomUserSearchAPIView.as_view(), name='api-search-user')
]
