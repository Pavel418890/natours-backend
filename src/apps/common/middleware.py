import re

from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.status import\
    HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


class Process500:
    """
    Обрабатывает 500 ошибку
     В случае создания нового пользователя с уже записанным в БД email адрессом
     добавлено человекочитаемое сообщение
    """

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):

        if isinstance(exception, IntegrityError)\
                and 'unique email' in exception.args[0]:

            raw_error_message_string = exception.args[0]

            email_str = re.findall(
                r'[\w\.-]+@[\w\.-]+', raw_error_message_string
            )[0]

            error_pattern = '{} has already exist. Please enter correct email.'

            return JsonResponse(
                {
                    'status': HTTP_400_BAD_REQUEST,
                    'errors': error_pattern.format(email_str)
                }
            )
        else:
            return JsonResponse({
                'status': HTTP_500_INTERNAL_SERVER_ERROR,
                'errors': f'{exception.__class__.__name__}({str(exception)})'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
