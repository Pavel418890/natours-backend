from django.urls import include, path

from ..views.users import (
    GetAllUsersView,
    GetUserByIdView,
    GetUserView,
    SignUpView,
    UpdateUserEmailView,
    ConfirmUserEmailView,
    UpdatePasswordView,
    ResetPasswordView,
)


users_url_pattern = (
    [
        path(
            route='',
            view=GetAllUsersView.as_view(),
            name='users'
        ),
        path(
            route='me/',
            view=GetUserView().as_view(),
            name='user-detail'
        ),
        path(
            route='<int:pk>/',
            view=GetUserByIdView().as_view(),
            name='user-detail-for-admin'
        ),
        path(
            route='signup/',
            view=SignUpView.as_view(),
            name='sign-up'
        ),
        path(
            route='update-email/',
            view=UpdateUserEmailView.as_view(),
            name='update-user-email'
        ),
        path(
            route='email-confirmation/<str:email_confirmation_token>/',
            view=ConfirmUserEmailView.as_view(),
            name='email-confirmation'
        ),
        path(
            route='update-password/',
            view=UpdatePasswordView.as_view(),
            name='update-user-password'
        ),
        path(
            route='reset-password/<str:password_reset_token>/',
            view=ResetPasswordView.as_view(),
            name='reset-user-password'
        ),
    ],
    'users'
)

urlpatterns = [
    path('users/', include(users_url_pattern)),
]
