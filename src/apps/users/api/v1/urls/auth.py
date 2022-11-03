from django.urls import include, path
from rest_framework_simplejwt.views import TokenVerifyView

from apps.users.api.v1.views import auth

auth_url_pattern = (
    [
        path(route="signin/", view=auth.SignInView.as_view(), name="login"),
        path(
            route="refresh-token/",
            view=auth.RefreshJWTView.as_view(),
            name="refresh-access-token",
        ),
        path(
            route="verify-token/", view=TokenVerifyView.as_view(), name="verify-token"
        ),
        path(
            route="forgot-password/",
            view=auth.ForgotPasswordView.as_view(),
            name="forgot-password",
        ),
    ],
    "auth",
)

urlpatterns = [
    path("auth/", include(auth_url_pattern)),
]
