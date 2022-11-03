from django.urls import include, path

from apps.users.api.v1.views import users

users_url_pattern = (
    [
        path(route="", view=users.GetAllUsersView.as_view(), name="users"),
        path(route="me/", view=users.GetUserView().as_view(), name="user-detail"),
        path(
            route="<int:pk>/",
            view=users.GetUserByIdView().as_view(),
            name="user-detail-for-admin",
        ),
        path(route="signup/", view=users.SignUpView.as_view(), name="sign-up"),
        path(
            route="update-email/",
            view=users.UpdateUserEmailView.as_view(),
            name="update-user-email",
        ),
        path(
            route="email-confirmation/<str:email_confirmation_token>/",
            view=users.ConfirmUserEmailView.as_view(),
            name="email-confirmation",
        ),
        path(
            route="update-password/",
            view=users.UpdatePasswordView.as_view(),
            name="update-user-password",
        ),
        path(
            route="reset-password/<str:password_reset_token>/",
            view=users.ResetPasswordView.as_view(),
            name="reset-user-password",
        ),
    ],
    "users",
)

urlpatterns = [
    path("users/", include(users_url_pattern)),
]
