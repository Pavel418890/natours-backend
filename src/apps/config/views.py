from django.http.response import HttpResponse
from rest_framework import permissions, views


class ProtectedDefaultRoute(views.APIView):
    """Проверяет статус авторизации пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return HttpResponse()
