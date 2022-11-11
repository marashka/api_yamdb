from rest_framework import status
from rest_framework.exceptions import APIException


class SecretKeyError(Exception):
    """Вызывается, когда отсутствует SECRET_KEY."""

    def __init__(self):
        super().__init__('Отсутствует SECRET_KEY.')


class WrongConfirmationCodeError(APIException):
    """Вызывается, когда confirmation code невалидный."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Предоставлен некорректный confirmation код'
    default_code = 'invalid_confirmation_code'
