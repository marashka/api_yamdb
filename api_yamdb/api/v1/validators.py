from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserValidator:
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        if get_object_or_None(User, username=value):
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        return value

    def validate_email(self, value):
        if get_object_or_None(User, email=value):
            raise serializers.ValidationError(
                'Пользователь с таким адрессом электронной '
                'почты уже существует.'
            )
        return value
