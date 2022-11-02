from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from apps.common.permissions import IsOwner, IsAdmin
from ..serializers.profile import (
    UpdateUserProfilePhotoSerializer,
    UpdateUserProfileSerializer,
    InMemoryUploadedFile
)


class UpdateProfilePhotoView(APIView):
    permission_classes = [IsAdmin | IsOwner]

    def put(self, request: Request) -> Response:
        serializer = UpdateUserProfilePhotoSerializer(
            request.user.profile, request.FILES
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)


class UpdateUserProfileView(APIView):
    permission_classes = [IsOwner | IsAdmin]

    def put(self, request: Request) -> Response:
        serializer = UpdateUserProfileSerializer(
            request.user.profile, request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)
