from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsOwner
from apps.users import services
from apps.users.api.v1.serializers.users import (
    SignUpSerializer, GetAllUsersSerializer, UpdateUserEmailSerializer, 
    ConfirmUserEmailSerializer, ResetPasswordSerializer, 
    UpdatePasswordSerializer, GetUserByIdSerializer,
)
from apps.users.api.v1.serializers.users import BaseUserSerializer
from apps.users.services.users_crud import UserCRUDService


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


class GetAllUsersView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request: Request) -> Response:
        users, count = UserCRUDService().get_all_users()
        serializer = GetAllUsersSerializer(users, many=True)
        return Response({"result": count, "data": serializer.data}, HTTP_200_OK)


class GetUserByIdView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request: Request, pk: int) -> Response:
        serializer = GetUserByIdSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, HTTP_200_OK)


class GetUserView(APIView):
    permission_classes = [IsOwner]

    def get(self, request: Request) -> Response:
        return Response(BaseUserSerializer(request.user).data, HTTP_200_OK)


class UpdateUserEmailView(APIView):
    permission_classes = [IsOwner]

    def put(self, request: Request) -> Response:
        serializer = UpdateUserEmailSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)


class ConfirmUserEmailView(APIView):
    permission_classes = [IsOwner]

    def put(self, request: Request, email_confirmation_token) -> Response:
        serializer = ConfirmUserEmailSerializer(
            instance=request.user,
            data={"email_confirmation_token": email_confirmation_token},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "detail": "You email address was confirmed."}, HTTP_200_OK
        )


class UpdatePasswordView(APIView):
    permission_classes = [IsOwner]

    def put(self, request: Request, *args, **kwargs) -> Response:
        serializer = UpdatePasswordSerializer(
            instance=self.request.user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"success": True, "detail": "Password was successfully updated"},
            status=HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, password_reset_token):
        serializer = ResetPasswordSerializer(
            data={**request.data, "password_reset_token": password_reset_token}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "detail": "Reset password completed"}, HTTP_200_OK
        )


class PseudoDeleteUserView(APIView):
    permission_classes = [IsOwner, IsAdmin]

    def delete(self, request):
        services.user.pseudo_delete_user(request.user)
        return Response(
            {
                "success": True,
                "detail": "Your account was deleted. "
                "You can always return to Natours Family - "
                "we will be wait for you!",
            },
            HTTP_204_NO_CONTENT,
        )
