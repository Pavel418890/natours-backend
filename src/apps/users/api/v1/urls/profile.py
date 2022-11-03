from django.urls import include, path

from apps.users.api.v1.views.profile import UpdateUserProfileView

profile_url_pattern = (
    [
        path(route="", view=UpdateUserProfileView.as_view(), name="update-profile"),
        path(
            route="update-photo/",
            view=UpdateUserProfileView.as_view(),
            name="update-profile-photo",
        ),
    ],
    "profile",
)

urlpatterns = [
    path("profile/", include(profile_url_pattern)),
]
