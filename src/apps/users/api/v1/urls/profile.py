from django.urls import include, path

from ..views.profile import UpdateUserProfileView, UpdateProfilePhotoView

profile_url_pattern = (
    [
        path(
            route='',
            view=UpdateUserProfileView.as_view(),
            name='update-profile'
        ),
        path(
            route='update-photo/',
            view=UpdateProfilePhotoView.as_view(),
            name='update-profile-photo'
        )

    ],
    'profile'
)

urlpatterns = [
    path('profile/', include(profile_url_pattern)),
]
