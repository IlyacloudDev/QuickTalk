from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling user creation, including regular users and superusers.
    
    Methods:
        create_user(phone_number, password=None, **extra_fields):
            Creates and saves a regular user with the provided phone number and password.
        
        create_superuser(phone_number, password=None, **extra_fields):
            Creates and saves a superuser with the provided phone number and password.
            Ensures that the superuser has is_staff=True and is_superuser=True.
    """
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and save a regular user with the given phone number and password.
        
        Args:
            phone_number (str): The user's phone number.
            password (str, optional): The user's password. Defaults to None.
            **extra_fields: Additional fields for the user.
        
        Returns:
            CustomUser: The created user instance.
        
        Raises:
            ValueError: If the phone number is not provided.
        """
        if not phone_number:
            raise ValueError(_('The Phone Number field must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create and save a superuser with the given phone number and password.
        
        Ensures that the superuser has is_staff=True and is_superuser=True.
        
        Args:
            phone_number (str): The superuser's phone number.
            password (str, optional): The superuser's password. Defaults to None.
            **extra_fields: Additional fields for the superuser.
        
        Returns:
            CustomUser: The created superuser instance.
        
        Raises:
            ValueError: If is_staff or is_superuser are not set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication using phone numbers instead of usernames.
    
    Fields:
        phone_number (PhoneNumberField): The user's unique phone number.
        username (CharField): The user's username, with a minimum length of 3 characters and a maximum of 15.
        avatar (ImageField): Optional user avatar, stored in the 'avatars/' directory.
        is_active (BooleanField): Indicates if the user's account is active.
        is_staff (BooleanField): Indicates if the user has staff privileges.
        date_joined (DateTimeField): Automatically records when the user account was created.
        
    Meta:
        verbose_name (str): Human-readable name for the model in the admin interface.
        verbose_name_plural (str): Human-readable plural name for the model in the admin interface.
    
    Methods:
        __str__: Returns the user's phone number as a string representation.
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
    REQUIRED_FIELDS = []  # No additional required fields

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        """
        String representation of the user, displaying their phone number.
        
        Returns:
            str: The user's phone number.
        """
        return str(self.phone_number)
