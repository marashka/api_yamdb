from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import MyUserManager
from .validators import CustomUsernameValidator


class User(AbstractUser):
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
            'Обязательное поле. Не более 150 символов.'
            'Только буквы, цифры и символы @/./+/-/_.'
        ),
        validators=[CustomUsernameValidator()],
        error_messages={
            'unique': _(
                'Пользователь с таким именем пользователя уже существует.'
            ),
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff
