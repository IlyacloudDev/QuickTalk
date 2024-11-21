from users.models import CustomUser
from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
import os
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


def _validate_password_for_minimum_length_and_character_complexity(password):
    """
    Ensures password meets length and complexity requirements.
    """
    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long."))

    if not re.search(r'\d', password):
        raise ValidationError(_("Password must contain at least one digit."))

    if not re.search(r'[A-Za-z]', password):
        raise ValidationError(_("Password must contain at least one letter."))
        
    return password


def _validate_two_password_fields_match(data):
    """
    Checks if the two password fields match.
    """
    if data.get('password') != data.get('password2'):
        raise serializers.ValidationError({
            "password": _("Passwords do not match."), 
            "password2": _("Passwords do not match.")
        })
    return data


def _create_new_customuser_instance_with_provided_data(phone_number, password):
    """
    Creates a new CustomUser instance.
    """
    user = CustomUser(phone_number=phone_number)
    user.set_password(password)
    user.save()
    return user


def _validate_phone_number_and_password_by_authenticating_user(phone_number, password):
    """
    Authenticates a user with the provided phone number and password.
    """
    if phone_number and password:
        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError({
                "phone_number": _('Invalid phone number or password'),
                "password": _('Invalid phone number or password')
            })
    return user  


def _update_customuser_instance_with_validated_data(instance, username, avatar):
    """
    Updates a CustomUser instance with the provided data.
    """
    instance.username = username
    user_own_avatar = avatar
    if user_own_avatar:
        if instance.avatar:
            old_avatar_path = instance.avatar.path
            instance.avatar = user_own_avatar
            os.remove(old_avatar_path)
        else:
            instance.avatar = user_own_avatar
    instance.save()
    return instance
