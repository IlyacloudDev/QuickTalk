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
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'password2']

    def validate_password(self, password):
        """
        Validates password length and complexity.
        """
        return _validate_password_for_minimum_length_and_character_complexity(password)

    def validate(self, data):
        """
        Ensures passwords match.
        """
        return _validate_two_password_fields_match(data)

    def create(self, validated_data):
        """
        Creates a new user instance.
        """
        validated_data.pop('password2')
        return _create_new_customuser_instance_with_provided_data(
            phone_number=validated_data.get('phone_number'), 
            password=validated_data.get('password')
        )


class LoginCustomUserSerializer(serializers.Serializer):
    """
    Serializer for user authentication.
    """
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Authenticates user by phone number and password.
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
    Serializer for user details.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'phone_number', 'id']


class CustomUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar']

    def update(self, instance, validated_data):
        """
        Updates user profile and avatar.
        """
        return _update_customuser_instance_with_validated_data(
            instance=instance, 
            username=validated_data.get('username', instance.username), 
            avatar=validated_data.get('avatar')
        )
