from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsOwner
from apps.users.api.v1 import serializers


class UpdateUserProfileView(APIView):
    permission_classes = [IsOwner | IsAdmin]

    def put(self, request: Request) -> Response:
        serializer = serializers.UpdateUserProfileSerializer(
            request.user.profile, request.FILES
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)
