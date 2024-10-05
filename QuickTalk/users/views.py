from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterCustomUserSerializer, LoginCustomUserSerializer, CustomUserProfileSerializer, CustomUserSearchSerializer, CustomUserSerializer
from django.contrib.auth import login
from django.contrib.auth import logout
from .permissions import IsOwner
from .models import CustomUser


class CustomUserCreateAPIView(APIView):
    """
    Handles user registration. Accepts POST requests with required user data (phone number, password, etc.).
    
    Returns:
    - 201 CREATED if user is successfully created with serialized data of the new user.
    - 400 BAD REQUEST if validation errors are found.
    """

    def post(self, request):
        serializer = RegisterCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                'new_user': RegisterCustomUserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomUserLoginAPIView(APIView):
    """
    Handles user login. Accepts POST requests with phone number and password.
    
    Returns:
    - 200 OK if login is successful.
    - 400 BAD REQUEST if login credentials are incorrect or missing.
    """

    def post(self, request):
        serializer = LoginCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"detail": _("Successfully logged in.")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserLogoutAPIView(APIView):
    """
    Handles user logout. Accepts POST requests to end the user session.
    
    Returns:
    - 200 OK if logout is successful.
    """

    def post(self, request):
        logout(request) 
        return Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)


class CustomUserSearchAPIView(APIView):
    """
    Allows authenticated users to search for other users by phone number. Accepts POST requests.
    
    Returns:
    - 200 OK with user details if the search is successful.
    - 404 NOT FOUND if the user does not exist.
    - 400 BAD REQUEST if validation errors are found.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomUserSearchSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            try:
                instance = CustomUser.objects.get(phone_number=phone_number)
                instance_serializer = CustomUserSerializer(instance).data
            except CustomUser.DoesNotExist:
                return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)
            if not instance_serializer['avatar']:
                instance_serializer['avatar'] = '/static/default_avatar/quicktalk_base-avatar.jpg'
        
            return Response({'detail': instance_serializer})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserUpdateAPIView(APIView):
    """
    Allows authenticated users to update their profile details (e.g., username, avatar).
    Accepts PUT requests with multipart/form-data.
    
    Returns:
    - 200 OK if the update is successful with the updated user data.
    - 404 NOT FOUND if the user does not exist.
    - 400 BAD REQUEST if validation errors are found.
    - 405 METHOD NOT ALLOWED if the PUT request does not include the user ID.
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
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
    Retrieves detailed information about a user based on the user ID (pk).
    Accepts GET requests.
    
    Returns:
    - 200 OK with user details if the user is found.
    - 404 NOT FOUND if the user does not exist.
    - 405 METHOD NOT ALLOWED if the request does not include the user ID.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": _("Method GET not allowed")}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = CustomUser.objects.get(pk=pk)
            instance_serializer = CustomUserSerializer(instance).data
        except CustomUser.DoesNotExist:
            return Response({"error": _("Object does not exist.")}, status=status.HTTP_404_NOT_FOUND)
        if not instance_serializer['avatar']:
            instance_serializer['avatar'] = '/static/default_avatar/quicktalk_base-avatar.jpg'
        return Response({'detail': instance_serializer})
