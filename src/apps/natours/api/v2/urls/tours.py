from django.urls import path

from ..views.tours import (
    GetAllTourView, CreateUpdateTourView, DeleteTourView, GetTourView,
)


urlpatterns = [
    path('', GetAllTourView.as_view(), name='tour-list'),
    path('new/', CreateUpdateTourView.as_view(), name='create-tour'),
    path('<int:pk>/', GetTourView.as_view(), name='tour-detail'),
    path('<slug:slug>/', GetTourView.as_view(), name='tour-detail'),
    path('delete/<int:pk>/', DeleteTourView.as_view(), name='delete-by-id'),
    path('delete/<slug:slug>/', DeleteTourView.as_view(), name='delete-by-slug'),
    path(
        'update/<int:pk>/',
        CreateUpdateTourView.as_view(),
        name='update-tour-by-id'
    ),
    path(
        'update/<slug:slug>/',
        CreateUpdateTourView.as_view(),
        name='update-tour-slug'
    ),
]