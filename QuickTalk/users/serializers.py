import re
from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
import os
from phonenumber_field.serializerfields import PhoneNumberField


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'password2']

    def validate_password(self, password):
        # Проверяем длину пароля
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))

        # Проверяем, содержит ли пароль хотя бы одну цифру
        if not re.search(r'\d', password):
            raise ValidationError(_("Password must contain at least one digit."))

        # Проверяем, содержит ли пароль хотя бы одну букву
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError(_("Password must contain at least one letter."))

    def validate(self, data):
        # Проверяем, что два пароля совпадают
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"password": _("Passwords do not match."), "password2": _("Passwords do not match.")})
        return data

    def create(self, validated_data):
        # Удаляем поле password2, так как оно не нужно для создания пользователя
        validated_data.pop('password2')
        user = CustomUser(
            phone_number=validated_data.get('phone_number'),
        )
        user.set_password(validated_data.get('password'))  # Хешируем пароль перед сохранением
        user.save()  # Сохраняем пользователя в базу данных
        return user


class LoginCustomUserSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user is None:
                raise serializers.ValidationError({"phone_number": _('Invalid phone number or password'), "password": _('Invalid phone number or password')})
        else:
            raise serializers.ValidationError({"phone_number": _('Both fields are required'), "password": _('Both fields are required')})

        data['user'] = user
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'phone_number', 'id']


class CustomUserSearchSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)

            
class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar']

    def update(self, instance, validated_data):
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
