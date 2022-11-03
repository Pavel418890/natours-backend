from django.urls import path

from apps.natours.api.v2.views import tours

urlpatterns = [
    path("", tours.GetAllTourView.as_view(), name="tour-list"),
    path("new/", tours.CreateUpdateTourView.as_view(), name="create-tour"),
    path("<int:pk>/", tours.GetTourView.as_view(), name="tour-detail"),
    path("<slug:slug>/", tours.GetTourView.as_view(), name="tour-detail"),
    path("delete/<int:pk>/", tours.DeleteTourView.as_view(), name="delete-by-id"),
    path("delete/<slug:slug>/", tours.DeleteTourView.as_view(), name="delete-by-slug"),
    path(
        "update/<int:pk>/",
        tours.CreateUpdateTourView.as_view(),
        name="update-tour-by-id",
    ),
    path(
        "update/<slug:slug>/",
        tours.CreateUpdateTourView.as_view(),
        name="update-tour-slug",
    ),
]
