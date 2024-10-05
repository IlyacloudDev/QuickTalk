from django.db import models
from users.models import CustomUser
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Chat(models.Model):
    """
    Represents a chat in the system, which can be either a personal chat between two users
    or a group chat with multiple participants. 

    Attributes:
        type (str): Specifies whether the chat is personal or group.
        created_by (CustomUser): The user who created the chat (only applicable for group chats).
        users (ManyToManyField): The users who are part of this chat.
        name (str): The name of the chat, used primarily for group chats.
        created_at (DateTimeField): The timestamp when the chat was created.
    """
    
    CHAT_TYPES = [
        ('personal', _('Personal')),
        ('group', _('Group')),
    ]
    
    type = models.CharField(
        verbose_name=_('Type'),
        max_length=10, 
        choices=CHAT_TYPES, 
    )
    created_by = models.ForeignKey(
        CustomUser, 
        verbose_name=_('Created by'),
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='created_chats', 
    )
    users = models.ManyToManyField(
        CustomUser, 
        verbose_name=_('Users'),
        related_name='chats', 
    )
    name = models.CharField(
        verbose_name=_('Name'), 
        max_length=30, 
        blank=False, 
        null=True, 
        validators=[MinLengthValidator(3)]
    )  
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True, 
    )

    def get_chat_name(self, current_user):
        """
        Returns the phone number of the other user in a personal chat, or the chat name for group chats.

        Args:
            current_user (CustomUser): The current user viewing the chat.

        Returns:
            str: The phone number of the other user for personal chats, or the chat name for group chats.
        """
        if self.type == 'personal':
            other_user = self.users.exclude(id=current_user.id).first()
            if other_user:
                return str(other_user.phone_number)
        return self.name

    def get_messages(self):
        """
        Retrieves all messages in the chat, ordered by the timestamp of when they were sent.

        Returns:
            QuerySet: A queryset of all messages in the chat, ordered by timestamp.
        """
        return self.messages.all().order_by('timestamp')

    def can_edit_or_delete(self, user):
        """
        Determines whether a user has permission to edit or delete the chat.

        Args:
            user (CustomUser): The user requesting permission.

        Returns:
            bool: True if the user can edit or delete the chat, False otherwise.
        """
        if self.type == 'group' and self.created_by == user:
            return True
        if self.type == 'personal' and user in self.users.all():
            return True
        return False

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')


class Message(models.Model):
    """
    Represents a message within a chat.

    Attributes:
        chat (Chat): The chat to which the message belongs.
        sender (CustomUser): The user who sent the message.
        content (str): The content of the message.
        timestamp (DateTimeField): The timestamp when the message was sent.
    """
    
    chat = models.ForeignKey(
        Chat, 
        on_delete=models.CASCADE, 
        related_name='messages', 
        verbose_name=_('Chat')
    )
    sender = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        verbose_name=_('Sender')
    )
    content = models.TextField(
        verbose_name=_('Content')
    )  
    timestamp = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Timestamp')
    )

    def get_sender_username(self):
        """
        Returns the username of the user who sent the message.

        Returns:
            str: The username of the sender.
        """
        return self.sender.username  

    class Meta:
        ordering = ['timestamp']
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
