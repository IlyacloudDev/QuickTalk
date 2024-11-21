from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import (
    RegisterCustomUserSerializer,
    LoginCustomUserSerializer,
    CustomUserProfileSerializer,
    CustomUserSerializer,
)
from django.contrib.auth import login, logout
from .permissions import IsOwner
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField


class CustomUserCreateAPIView(APIView):
    """
    Handles user registration.
    """
    def post(self, request):
        serializer = RegisterCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"new_user": RegisterCustomUserSerializer(user).data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserLoginAPIView(APIView):
    """
    Handles user login.
    """
    def post(self, request):
        serializer = LoginCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            login(request, serializer.validated_data['user'])
            return Response({"detail": _("Successfully logged in.")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserLogoutAPIView(APIView):
    """
    Handles user logout.
    """
    def post(self, request):
        logout(request)
        return Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)


class CustomUserSearchAPIView(APIView):
    """
    Searches for a user by phone number.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('query', '')
        if search_query:
            phone_field = PhoneNumberField()
            try:
                phone_field.run_validation(search_query)
            except ValidationError as e:
                return Response({"error": e.detail[0]}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user_item = CustomUser.objects.get(phone_number=search_query)
            except CustomUser.DoesNotExist:
                return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CustomUserSerializer(user_item).data
        if not serializer['avatar']:
            serializer['avatar'] = '/static/default_avatar/quicktalk_base-avatar.jpg'
        return Response(serializer)


class CustomUserUpdateAPIView(APIView):
    """
    Updates user profile details.
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return Response({"error": _("Method PUT not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserProfileSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailAPIView(APIView):
    """
    Retrieves user details by ID.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return Response({"error": _("Method GET not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(instance).data
        except CustomUser.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)
        if not serializer['avatar']:
            serializer['avatar'] = '/static/default_avatar/quicktalk_base-avatar.jpg'
        return Response({'detail': serializer})
