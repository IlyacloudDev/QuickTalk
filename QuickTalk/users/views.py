from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterCustomUserSerializer, LoginCustomUserSerializer, CustomUserProfileSerializer, CustomUserSearchSerializer, CustomUserSerializer
from django.contrib.auth import login
from django.contrib.auth import logout
from .permissions import IsOwner
from .models import CustomUser


class CustomUserCreateAPIView(APIView):
    def post(self, request):
        serializer = RegisterCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Возвращаем сериализованные данные о созданном пользователе
            return Response(
                {
                'new_user': RegisterCustomUserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomUserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Авторизация пользователя
            return Response({"detail": "Successfully logged in."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserLogoutAPIView(APIView):
    def post(self, request):
        # Завершение сессии
        logout(request)
        # Возвращаем успешный ответ
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class CustomUserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomUserSearchSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            try:
                instance = CustomUser.objects.get(phone_number=phone_number)
                instance_serializer = CustomUserSerializer(instance).data
            except CustomUser.DoesNotExist:
                return Response({"error": "Object does not exist."}, status=status.HTTP_404_NOT_FOUND)
            if not instance_serializer['avatar']:
                instance_serializer['avatar'] = '/static/default_avatar/quicktalk_base-avatar.jpg'
        
            return Response({'detail': instance_serializer})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserUpdateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserProfileSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = CustomUser.objects.get(pk=pk)
            instance_serializer = CustomUserSerializer(instance).data
        except CustomUser.DoesNotExist:
            return Response({"error": "Object does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if not instance_serializer['avatar']:
            instance_serializer['avatar'] = '/static/default_avatar/quicktalk_base-avatar.jpg'
        return Response({'detail': instance_serializer})
