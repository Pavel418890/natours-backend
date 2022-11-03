from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.v1.serializers.auth import (
    ForgotPasswordSerializer, RefreshJWTSerializer, SignInSerializer
)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)


class RefreshJWTView(TokenRefreshView):
    serializer_class = RefreshJWTSerializer


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": "Please check your mail.We have sent"
                " further instructions to your email."
            },
            HTTP_200_OK,
        )
