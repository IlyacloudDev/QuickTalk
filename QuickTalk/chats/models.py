from django.db import models
from users.models import CustomUser
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Chat(models.Model):
    """
    Represents a chat in the system.
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

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')


class Message(models.Model):
    """
    Represents a message in a chat.
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

    class Meta:
        ordering = ['timestamp']
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
