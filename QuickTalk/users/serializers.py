import re
from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
import os
from phonenumber_field.serializerfields import PhoneNumberField


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new CustomUser. Includes password validation and a repeated password check.
    
    Fields:
        - phone_number: User's phone number (required).
        - password: User's password (write-only, required).
        - password2: Confirmation of the user's password (write-only, required).
    
    Methods:
        validate_password(password):
            Validates that the password meets minimum length and complexity requirements.
        
        validate(data):
            Ensures that both password fields match.
        
        create(validated_data):
            Creates a new CustomUser instance and saves it with the hashed password.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'password2']

    def validate_password(self, password):
        """
        Validates the password for minimum length and character complexity.
        
        Args:
            password (str): The password provided by the user.
        
        Raises:
            ValidationError: If the password does not meet the required length or complexity.
        
        Returns:
            str: The validated password.
        """
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))

        if not re.search(r'\d', password):
            raise ValidationError(_("Password must contain at least one digit."))

        if not re.search(r'[A-Za-z]', password):
            raise ValidationError(_("Password must contain at least one letter."))
        
        return password

    def validate(self, data):
        """
        Validates that the two password fields match.
        
        Args:
            data (dict): The data containing the passwords.
        
        Raises:
            serializers.ValidationError: If the passwords do not match.
        
        Returns:
            dict: The validated data.
        """
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({
                "password": _("Passwords do not match."), 
                "password2": _("Passwords do not match.")
            })
        return data

    def create(self, validated_data):
        """
        Creates a new CustomUser instance with the provided data.
        
        Args:
            validated_data (dict): The validated data for creating the user.
        
        Returns:
            CustomUser: The created user instance.
        """
        validated_data.pop('password2')
        user = CustomUser(phone_number=validated_data.get('phone_number'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class LoginCustomUserSerializer(serializers.Serializer):
    """
    Serializer for authenticating a CustomUser via phone number and password.
    
    Fields:
        - phone_number: User's phone number (required).
        - password: User's password (write-only, required).
    
    Methods:
        validate(data):
            Authenticates the user using the provided credentials.
    """
    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Validates the phone number and password by authenticating the user.
        
        Args:
            data (dict): The data containing the phone number and password.
        
        Raises:
            serializers.ValidationError: If the phone number or password is incorrect or not provided.
        
        Returns:
            dict: The validated data with the authenticated user included.
        """
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user is None:
                raise serializers.ValidationError({
                    "phone_number": _('Invalid phone number or password'),
                    "password": _('Invalid phone number or password')
                })
        else:
            raise serializers.ValidationError({
                "phone_number": _('Both fields are required'),
                "password": _('Both fields are required')
            })

        data['user'] = user
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model, returning basic user information.
    
    Fields:
        - username: User's username.
        - avatar: User's avatar image.
        - phone_number: User's phone number.
        - id: User's unique ID.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'phone_number', 'id']


class CustomUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the profile of a CustomUser, allowing modifications to the username and avatar.
    
    Fields:
        - username: User's username.
        - avatar: User's avatar image.
    
    Methods:
        update(instance, validated_data):
            Updates the user's profile with the provided data, and handles avatar updates.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar']

    def update(self, instance, validated_data):
        """
        Updates the CustomUser instance with the validated data.
        
        Args:
            instance (CustomUser): The user instance to be updated.
            validated_data (dict): The validated data containing the fields to update.
        
        Returns:
            CustomUser: The updated user instance.
        """
        instance.username = validated_data.get('username', instance.username)
        user_own_avatar = validated_data.get('avatar')
        if user_own_avatar:
            if instance.avatar:
                old_avatar_path = instance.avatar.path
                instance.avatar = user_own_avatar
                os.remove(old_avatar_path)
            else:
                instance.avatar = user_own_avatar
        instance.save()
        return instance
