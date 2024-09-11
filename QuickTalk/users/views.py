from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterCustomUserSerializer, LoginCustomUserSerializer
from rest_framework.response import Response
from django.contrib.auth import login


class CustomUserCreateAPIView(APIView):
    def post(self, request):
        serializer = RegisterCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Возвращаем сериализованные данные о созданном пользователе
            return Response(RegisterCustomUserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomUserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginCustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)  # Авторизация пользователя
            return Response({"detail": "Successfully logged in."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
