from django.urls import path
from .views import CustomUserLoginAPIView, CustomUserCreateAPIView, CustomUserUpdateAPIView

urlpatterns = [
    path('login/', CustomUserLoginAPIView.as_view(), name='api-login'),
    path('register/', CustomUserCreateAPIView.as_view(), name='api-register'),
    path('update-user/<int:pk>/', CustomUserUpdateAPIView.as_view(), name='api-update-user')
]