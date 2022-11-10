from rest_framework import status
from rest_framework.exceptions import APIException


class SecretKeyError(Exception):
    """Вызывается, когда хотя бы один из токенов невалидный."""

    def __init__(self):
        super().__init__('Отсутствуют один или несколько токенов.')


class WrongConfirmationCodeError(APIException):
    """Вызывается, когда хотя бы один из токенов невалидный."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Предоставлен некорректный confirmation код'
    default_code = 'invalid_confirmation_code'
