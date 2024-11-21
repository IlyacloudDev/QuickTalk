from rest_framework import serializers
from .services.chats_serializers_services import (
    _create_group_chat_and_add_requesting_user_as_participant,
    _update_name_of_existing_group_chat,
    _validate_personal_chat_between_requesting_user_and_chosen_user,
    _create_personal_chat_between_requesting_user_and_chosen_user,
    _get_username_of_user_who_sent_message,
    _get_chat_name_or_phone_number_for_personal_chat,
    _get_all_messages_from_chat,
    _permission_delete_update_chat,
    _delete_chat,
    _validate_process_user_join_to_group_chat
)
from .models import Chat, Message
from django.utils.translation import gettext_lazy as _


class CreateGroupChatSerializer(serializers.ModelSerializer):
    """
    Handles creation and updates for group chats.
    """
    type = serializers.CharField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chat
        fields = ['name', 'type', 'created_by', 'created_at']

    def create(self, validated_data):
        request_user = self.context['request'].user
        return _create_group_chat_and_add_requesting_user_as_participant(
            created_by=request_user,
            name=validated_data.get('name')
        )
    
    def update(self, instance, validated_data):
        return _update_name_of_existing_group_chat(
            instance=instance,
            name=validated_data.get('name', instance.name)
        )


class CreatePersonalChatSerializer(serializers.ModelSerializer):
    """
    Creates personal chats between two users.
    """
    type = serializers.CharField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    chosen_user_to_prsnl_cht_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chat
        fields = ['name', 'type', 'created_by', 'created_at', 'chosen_user_to_prsnl_cht_id']

    def validate(self, data):
        return _validate_personal_chat_between_requesting_user_and_chosen_user(
            data=data,
            request_user=self.context['request'].user,
            pk=data['chosen_user_to_prsnl_cht_id']
        )

    def create(self, validated_data):
        return _create_personal_chat_between_requesting_user_and_chosen_user(
            request_user=self.context['request'].user,
            other_user_id=validated_data.pop('chosen_user_to_prsnl_cht_id')
        )


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializes messages, including sender's username.
    """
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender', 'sender_username']

    def get_sender_username(self, obj):
        return _get_username_of_user_who_sent_message(obj=obj)


class ChatsListSerializer(serializers.ModelSerializer):
    """
    Lists chats with details, messages, and permissions.
    """
    chat_name = serializers.SerializerMethodField()
    messages_of_chat = serializers.SerializerMethodField()
    permission_delete_update_chat = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['chat_name', 'messages_of_chat', 'permission_delete_update_chat', 'type', 'id']

    def get_chat_name(self, obj):
        user = self.context['request'].user
        return _get_chat_name_or_phone_number_for_personal_chat(
            obj=obj,
            current_user=user
        )

    def get_messages_of_chat(self, obj):
        messages = _get_all_messages_from_chat(obj=obj)
        return MessageSerializer(messages, many=True).data
    
    def get_permission_delete_update_chat(self, obj):
        user = self.context['request'].user
        return _permission_delete_update_chat(obj=obj, request_user=user)


class ChatDeleteSerializer(serializers.ModelSerializer):
    """
    Deletes a chat instance.
    """
    
    class Meta:
        model = Chat
        fields = []

    def destroy(self, instance):
        _delete_chat(instance=instance)
        return


class JoinToGroupChatSerializer(serializers.Serializer):
    """
    Validates and processes user join requests for group chats.
    """
    user_id_to_join = serializers.IntegerField(required=True)
    chat_id_to_join = serializers.IntegerField(required=True)

    def validate(self, data):
        return _validate_process_user_join_to_group_chat(data=data)
