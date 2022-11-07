from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import MyUserManager
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    regex = r'^(?!me\b)[\w.@+-]+$'
    message = (
        'Имя пользователя может содержать только буквы, цифры и символы '
        '@/./+/-/_. Использовать имя "me" в качестве username запрещено'
    )
    flags = 0


class User(AbstractUser):
    username_validator = CustomUsernameValidator()
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    ]
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=200,
        choices=ROLES_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    objects = MyUserManager()

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
