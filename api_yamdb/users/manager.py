from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Имя пользователя должно быть установлено')
        if not email:
            raise ValueError('Пользователь должен иметь электронную почту')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
# мы не используем в модели юзера этот миксин: 
# https://django.fun/ru/docs/django/4.1/topics/auth/customizing/#custom-users-and-permissions
# значит это очень грубая ошибка, когда не очевидным для нас способов в класс 
# устанавливается дополнительный аттрибут в нашем случае из супер юзер.
# и тут либо убирать либо дописывать в зависимости от того нужно ли вам работа с разрешениями джанги.
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
# аналогично
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперюзер должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперюзер должен иметь is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)
