from django.urls import path

from apps.natours.api.v1.views.tours import ToursToMonthAPIView, \
    TourStatisticsAPIView, Top5CheapTourAPIView

urlpatterns = [

    path(
        'monthly-plan/<int:year>/',
        ToursToMonthAPIView.as_view(),
        name='tour-monthly-plan'
    ),
    path(
        'tour-stat/',
        TourStatisticsAPIView.as_view(),
        name='tour-stat'
    ),
    path(
        'top-5-cheap-tour/',
        Top5CheapTourAPIView.as_view(),
        name='top-5-cheap-tour'
    ),
]
