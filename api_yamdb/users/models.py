from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'US'
    ADMIN = 'AD'
    MODERATOR = 'MO'
    ROLES_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=2,
        choices=ROLES_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
