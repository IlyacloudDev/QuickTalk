from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
import random
import string


def generate_username():
    # Генерируем строку из 6 случайных символов (буквы и цифры)
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return 'user_' + random_chars


@receiver(post_save, sender=CustomUser)
def add_avatar_and_username(instance, created, **kwargs):
    if not created:
        return
    instance.username = generate_username()
    instance.save(update_fields=['username'])
