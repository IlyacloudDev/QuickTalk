from rest_framework import serializers
from .services.users_serializers_services import (
    _validate_password_for_minimum_length_and_character_complexity,
    _validate_two_password_fields_match,
    _create_new_customuser_instance_with_provided_data,
    _validate_phone_number_and_password_by_authenticating_user,
    _update_customuser_instance_with_validated_data
)
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
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
        Validates the password to ensure it meets minimum length and complexity requirements.

        Args:
            password (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            serializers.ValidationError: If the password does not meet the required criteria.
        """
        return _validate_password_for_minimum_length_and_character_complexity(password)
        

    def validate(self, data):
        """
        Validates the data to ensure the passwords match.

        Args:
            data (dict): The data containing the passwords.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        return _validate_two_password_fields_match(data)
        

    def create(self, validated_data):
        """
        Creates a new CustomUser instance with the provided data.

        Args:
            validated_data (dict): The validated data, excluding the repeated password field.

        Returns:
            CustomUser: The newly created user instance.
        """
        validated_data.pop('password2')
        return _create_new_customuser_instance_with_provided_data(
            phone_number=validated_data.get('phone_number'), 
            password=validated_data.get('password')
        )


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
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Authenticates the user with the provided phone number and password.

        Args:
            data (dict): The data containing phone number and password.

        Returns:
            dict: The validated data with the authenticated user.

        Raises:
            serializers.ValidationError: If authentication fails.
        """
        phone_number = data.get('phone_number')
        password = data.get('password')

        data['user'] = _validate_phone_number_and_password_by_authenticating_user(
            phone_number=phone_number, 
            password=password
        )
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
        Updates the CustomUser instance with the provided data.

        Args:
            instance (CustomUser): The CustomUser instance to update.
            validated_data (dict): The validated data for updating the user.

        Returns:
            CustomUser: The updated user instance.
        """
        return _update_customuser_instance_with_validated_data(
            instance=instance, 
            username=validated_data.get('username', instance.username), 
            avatar=validated_data.get('avatar')
        )
