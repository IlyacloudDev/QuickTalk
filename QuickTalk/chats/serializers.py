from rest_framework import serializers
from .models import Chat, Message
from users.models import CustomUser
from .exceptions import AlreadyJoinedChatException
from django.utils.translation import gettext_lazy as _


class CreateGroupChatSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a group chat. Automatically sets the chat type to 'group'
    and associates the chat with the user making the request.

    Fields:
        name (str): The name of the group chat.
        type (str): The type of the chat, which is 'group' (read-only).
        created_by (CustomUser): The user who created the chat (read-only).
        created_at (DateTimeField): The timestamp of chat creation (read-only).
    """
    type = serializers.CharField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chat
        fields = ['name', 'type', 'created_by', 'created_at']

    def create(self, validated_data):
        """
        Creates a new group chat and adds the requesting user as a participant.

        Args:
            validated_data (dict): Validated data from the request.

        Returns:
            Chat: The created group chat instance.
        """
        request_user = self.context['request'].user
        chat = Chat.objects.create(
            type='group',  
            created_by=request_user,
            name=validated_data.get('name'),
        )
        chat.users.add(request_user)
        return chat
    
    def update(self, instance, validated_data):
        """
        Updates the name of an existing group chat.

        Args:
            instance (Chat): The chat instance being updated.
            validated_data (dict): Validated data from the request.

        Returns:
            Chat: The updated chat instance.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class CreatePersonalChatSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a personal chat between two users. Validates that the chat does not already exist.

    Fields:
        name (str): Optional name for the personal chat (usually not used).
        type (str): The type of the chat, which is 'personal' (read-only).
        created_by (CustomUser): The user who created the chat (read-only).
        created_at (DateTimeField): The timestamp of chat creation (read-only).
        chosen_user_to_prsnl_cht_id (int): The ID of the other user in the personal chat (write-only).
    """
    type = serializers.CharField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    chosen_user_to_prsnl_cht_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chat
        fields = ['name', 'type', 'created_by', 'created_at', 'chosen_user_to_prsnl_cht_id']

    def validate(self, data):
        """
        Validates that a personal chat between the requesting user and the chosen user does not already exist.

        Args:
            data (dict): Validated data from the request.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If a personal chat between the users already exists.
        """
        request_user = self.context['request'].user
        other_user = CustomUser.objects.get(pk=data['chosen_user_to_prsnl_cht_id'])
        
        existing_chat = Chat.objects.filter(
            type='personal',
            users=request_user
        ).filter(users=other_user).exists()

        if existing_chat:
            raise serializers.ValidationError(_("A personal chat between these users already exists."))
        return data

    def create(self, validated_data):
        """
        Creates a new personal chat between the requesting user and another user.

        Args:
            validated_data (dict): Validated data from the request.

        Returns:
            Chat: The created personal chat instance.
        """
        request_user = self.context['request'].user
        other_user_id = validated_data.pop('chosen_user_to_prsnl_cht_id')
        other_user = CustomUser.objects.get(pk=other_user_id)
        chat = Chat.objects.create(
            type='personal',
            created_by=request_user,
        )
        chat.users.add(request_user, other_user)
        return chat


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for chat messages. Provides additional information about the sender's username.

    Fields:
        id (int): The ID of the message.
        content (str): The content of the message.
        timestamp (DateTimeField): The timestamp of when the message was sent.
        sender (CustomUser): The user who sent the message.
        sender_username (str): The username of the sender (read-only).
    """
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender', 'sender_username']

    def get_sender_username(self, obj):
        """
        Retrieves the username of the user who sent the message.

        Args:
            obj (Message): The message instance.

        Returns:
            str: The username of the sender.
        """
        return obj.get_sender_username()


class ChatsListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing chats. Provides chat details, recent messages, and user permissions.

    Fields:
        chat_name (str): The name of the chat or the phone number of the other user in a personal chat.
        messages_of_chat (list): A list of messages in the chat.
        permission_delete_update_chat (bool): Whether the user has permission to delete or update the chat.
        type (str): The type of the chat (personal or group).
        id (int): The ID of the chat.
    """
    chat_name = serializers.SerializerMethodField()
    messages_of_chat = serializers.SerializerMethodField()
    permission_delete_update_chat = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['chat_name', 'messages_of_chat', 'permission_delete_update_chat', 'type', 'id']

    def get_chat_name(self, obj):
        """
        Retrieves the chat name or, for personal chats, the phone number of the other user.

        Args:
            obj (Chat): The chat instance.

        Returns:
            str: The chat name or the other user's phone number.
        """
        user = self.context['request'].user
        return obj.get_chat_name(user)
    
    def get_messages_of_chat(self, obj):
        """
        Retrieves the messages for the given chat, serialized as a list of message data.

        Args:
            obj (Chat): The chat instance.

        Returns:
            list: A list of serialized messages in the chat.
        """
        messages = obj.get_messages()
        return MessageSerializer(messages, many=True).data
    
    def get_permission_delete_update_chat(self, obj):
        """
        Determines whether the user has permission to delete or update the chat.

        Args:
            obj (Chat): The chat instance.

        Returns:
            bool: True if the user can delete or update the chat, False otherwise.
        """
        user = self.context['request'].user
        return obj.can_edit_or_delete(user)


class ChatDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for deleting a chat. It contains no fields and simply handles the deletion of the chat instance.
    """
    
    class Meta:
        model = Chat
        fields = []

    def destroy(self, instance):
        """
        Deletes the chat instance.

        Args:
            instance (Chat): The chat instance to be deleted.
        """
        instance.delete()
        return


class JoinToGroupChatSerializer(serializers.Serializer):
    """
    Serializer to validate and process user join requests for a group chat.

    Fields:
        - user_id_to_join (IntegerField): ID of the user who is requesting to join the chat. Required.
        - chat_id_to_join (IntegerField): ID of the chat to be joined. Required.

    Validation:
        - Checks if both the user and chat with the provided IDs exist.
        - If either the user or chat does not exist, raises a ValidationError with the message "Object does not exist."
        - Verifies if the user is already a member of the chat.
            - If the user is already in the chat, raises an `AlreadyJoinedChatException`.
            - Otherwise, adds the user to the chat.

    Returns:
        - The validated data if the user is successfully added to the chat.

    Raises:
        - ValidationError: If the specified user or chat does not exist.
        - AlreadyJoinedChatException: If the user is already a member of the specified chat.
    """
    user_id_to_join = serializers.IntegerField(required=True)
    chat_id_to_join = serializers.IntegerField(required=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(id=data['user_id_to_join'])
            chat = Chat.objects.get(id=data['chat_id_to_join'])

        except (Chat.DoesNotExist, CustomUser.DoesNotExist):
            raise serializers.ValidationError(_("Object does not exist."))

        already_joined = chat.users.filter(id=user.id).exists()

        if already_joined:
            raise AlreadyJoinedChatException()
        chat.users.add(user)
        return data
