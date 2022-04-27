from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView

from ..views.auth import (
    SignInView,
    RefreshJWTView,
    ForgotPasswordView,
)

auth_url_pattern = (
    [
        path(
            route='signin/',
            view=SignInView.as_view(),
            name='login'
        ),
        path(
            route='refresh-token/',
            view=RefreshJWTView.as_view(),
            name='refresh-access-token'
        ),
        path(
            route='verify-token/',
            view=TokenVerifyView.as_view(),
            name='verify-token'
        ),

        path(
            route='forgot-password/',
            view=ForgotPasswordView.as_view(),
            name='forgot-password'
        ),


    ],
    'auth'
)

urlpatterns = [
    path('auth/', include(auth_url_pattern)),
]
