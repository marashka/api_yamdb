import datetime
import functools
import inspect
import json
import traceback

from django.db import transaction
from django.http import JsonResponse
from django.views import View

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=200):
    """Отдаёт JSON с правильнымы HTTP заголовками и в читаемом
    в браузере виде в случае с кирилицей"""
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    """Формирует HTTP ответ с описанием ошибки и Traceback'ом"""
    res = {
        'errorMessage': str(exception),
        'traceback': traceback.format_exc()
    }
    return ret(res, status=400)


def base_view(func):
    """Декоратор для всех вьюшек, обрабатывет исключения"""
    @functools.wraps
    def wrapper(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return func(request, *args, **kwargs)
        except Exception as error:
            return error_response(error)
    return wrapper

