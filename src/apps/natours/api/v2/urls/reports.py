from django.urls import path

from apps.natours.api.v2.views.tour_report import (
    year_report_2021,
    year_report_2022,
    cheapest_5_tours,
    tours_statistics_by_difficulty,
)


urlpatterns = [

    path('year-report/2021/', year_report_2021, name='2021-year-report'),
    path('year-report/2022/', year_report_2022, name='2022-year-report'),
    path('tour-stat/', tours_statistics_by_difficulty, name='tour-stat'),
    path('top-5-cheap-tour/', cheapest_5_tours, name='top-5-cheap-tour'),
]
