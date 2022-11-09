from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .manager import MyUserManager


@deconstructible
# Убираем в файл валидаторс пай.
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
# пишем русский ресурс, так что все на русском.
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
# переносим в стиле джанго
    role = models.CharField(
        max_length=10,
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
# в админы можно посчитать и супер юзеров и тех кто имеет флаг из стаф 
# но в нашем случае из супер юзера нет так как не используется миски соответствующий.
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
# Нарушен код стайл Джанго.
# The order of model inner classes and standard methods should be as follows (noting that these are not all required):
# All database fields
# Custom manager attributes
# class Meta
# def __str__()
# def save()
# def get_absolute_url()
# Any custom methods
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
