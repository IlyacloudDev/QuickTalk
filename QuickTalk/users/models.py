from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
    Manager for creating regular users and superusers.
    """
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a user with a phone number and password.
        """
        if not phone_number:
            raise ValueError(_('The Phone Number field must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with required privileges.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using phone numbers for authentication.
    """
    phone_number = PhoneNumberField(
        verbose_name=_('Phone number'),
        unique=True
    )
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=15,
        blank=False,
        validators=[MinLengthValidator(3)]
    )
    avatar = models.ImageField(
        verbose_name=_('Avatar of user'), 
        upload_to='avatars/', 
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_('Active'), 
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name=_('Staff status'), 
        default=False
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        auto_now_add=True
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        """
        Returns the phone number as the string representation.
        """
        return str(self.phone_number)
