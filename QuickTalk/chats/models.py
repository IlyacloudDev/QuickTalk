from django.db import models
from users.models import CustomUser
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Chat(models.Model):
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
        """Возвращает номер телефона другого пользователя для личного чата."""
        if self.type == 'personal':
            # Найдем другого пользователя
            other_user = self.users.exclude(id=current_user.id).first()
            if other_user:
                return str(other_user.phone_number)  # Отображаем номер телефона собеседника
        return self.name  # Для групповых чатов возвращаем имя, если оно установлено

    def get_messages(self):
        return self.messages.all().order_by('-timestamp')

    def can_edit_or_delete(self, user):
        """Проверяет, может ли пользователь редактировать или удалять чат."""
        if self.type == 'group' and self.created_by == user:
            return True
        if self.type == 'personal' and user in self.users.all():
            return True
        return False

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')


class Message(models.Model):
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
        )  # Поле для хранения текста сообщения
    timestamp = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Timestamp')
        )  # Автоматическое добавление времени отправки

    class Meta:
        ordering = ['timestamp']  # Сообщения будут сортироваться по времени отправки
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
