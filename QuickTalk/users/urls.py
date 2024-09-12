from django.urls import path
from .views import CustomUserLoginAPIView, CustomUserCreateAPIView

urlpatterns = [
    path('login/', CustomUserLoginAPIView.as_view(), name='api-login'),
    path('register/', CustomUserCreateAPIView.as_view(), name='api-register')
]