from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import MyUserManager


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    ]

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
        return self.role == self.ADMIN or (self.is_superuser and self.is_staff)

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
