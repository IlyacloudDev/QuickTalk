from rest_framework import serializers
from chats.models import Chat
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


def _create_group_chat_and_add_requesting_user_as_participant(created_by, name):
    """
    Creates a group chat and adds the creator as a participant.
    """
    chat = Chat.objects.create(
        type='group',
        created_by=created_by,
        name=name,
    )
    chat.users.add(created_by)
    return chat    


def _update_name_of_existing_group_chat(instance, name):
    """
    Updates the name of a group chat.
    """
    instance.name = name
    instance.save()
    return instance


def _validate_personal_chat_between_requesting_user_and_chosen_user(data, request_user, pk):
    """
    Validates that a personal chat does not already exist.
    """
    other_user = CustomUser.objects.get(pk=pk)

    if Chat.objects.filter(
        type='personal',
        users=request_user
    ).filter(users=other_user).exists():
        raise serializers.ValidationError(_("A personal chat between these users already exists."))
    return data


def _create_personal_chat_between_requesting_user_and_chosen_user(request_user, other_user_id):
    """
    Creates a personal chat between two users.
    """
    other_user = CustomUser.objects.get(pk=other_user_id)
    chat = Chat.objects.create(
        type='personal',
        created_by=request_user,
    )
    chat.users.add(request_user, other_user)
    return chat


def _get_username_of_user_who_sent_message(obj):
    """
    Returns the username of the message sender.
    """
    return obj.sender.username


def _get_chat_name_or_phone_number_for_personal_chat(obj, current_user):
    """
    Retrieves the name or phone number for a personal chat.
    """
    if obj.type == 'personal':
        other_user = obj.users.exclude(id=current_user.id).first()
        if other_user:
            return str(other_user.phone_number)
    return obj.name


def _get_all_messages_from_chat(obj):
    """
    Returns all messages from a chat ordered by timestamp.
    """
    return obj.messages.all().order_by('timestamp')


def _permission_delete_update_chat(obj, request_user):
    """
    Checks if a user has permission to delete or update a chat.
    """
    if obj.type == 'group' and obj.created_by == request_user:
        return True
    if obj.type == 'personal' and request_user in obj.users.all():
        return True
    return False


def _delete_chat(instance):
    """
    Deletes a chat instance.
    """
    instance.delete()


def _validate_process_user_join_to_group_chat(data):
    """
    Validates and processes a user joining a group chat.
    """
    user = CustomUser.objects.get(id=data['user_id_to_join'])
    chat = Chat.objects.get(id=data['chat_id_to_join'])
    if chat.users.filter(id=user.id).exists():
        raise serializers.ValidationError(_('The user has already joined this group chat.'))
    chat.users.add(user)
    return data
