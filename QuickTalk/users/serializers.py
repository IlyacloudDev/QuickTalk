from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password']

    def create(self, validated_data):
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
                raise serializers.ValidationError(_('Invalid phone number or password'))
        else:
            raise serializers.ValidationError(_('Both fields are required'))

        data['user'] = user
        return data

