from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Chat(models.Model):
    CHAT_TYPES = [
        ('personal', _('Personal')),
        ('group', _('Group')),
    ]
    
    type = models.CharField(max_length=10, choices=CHAT_TYPES, verbose_name=_('Type'))
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='created_chats', verbose_name=_('Created by'))
    users = models.ManyToManyField(CustomUser, related_name='chats', verbose_name=_('Users'))
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Name'))  # Только для групповых чатов
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def clean(self):
        """Проверка на наличие уже существующего личного чата между пользователями."""
        if self.type == 'personal':
            # Получаем пользователей, которые участвуют в чате
            users_in_chat = self.users.all()
            if users_in_chat.count() == 2:  # Личный чат состоит из двух пользователей
                user1, user2 = users_in_chat
                # Проверяем, существует ли личный чат с этими пользователями
                existing_chat = Chat.objects.filter(type='personal', users=user1).filter(users=user2).exists()
                if existing_chat:
                    raise ValidationError(_("A personal chat between these users already exists."))
            else:
                raise ValidationError(_("A personal chat can only be between two users."))

    def save(self, *args, **kwargs):
        """Переопределение сохранения с предварительной валидацией."""
        self.full_clean()  # Вызываем метод clean для валидации перед сохранением
        super().save(*args, **kwargs)

    def get_chat_name(self, current_user):
        """Возвращает имя чата для личного чата, основываясь на текущем пользователе."""
        if self.type == 'personal':
            # Найдем другого пользователя
            other_user = self.users.exclude(id=current_user.id).first()
            return other_user.username
        return self.name  # Для групповых чатов возвращаем имя, если оно установлено

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
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Chat'))
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Sender'))
    content = models.TextField(verbose_name=_('Content'))  # Поле для хранения текста сообщения
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))  # Автоматическое добавление времени отправки

    class Meta:
        ordering = ['timestamp']  # Сообщения будут сортироваться по времени отправки
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
