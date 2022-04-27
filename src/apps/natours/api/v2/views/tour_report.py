from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from apps.natours.models import Tour
from apps.natours.models.tour_report import R2022, R2021


@api_view(http_method_names=['GET'])
def year_report_2021(request):
    return Response(Tour.report.get_year_report(R2021), HTTP_200_OK)


@api_view(http_method_names=['GET'])
def year_report_2022(request):
    return Response(Tour.report.get_year_report(R2022), HTTP_200_OK)


@api_view(http_method_names=['GET'])
def cheapest_5_tours(request):
    return Response(Tour.report.get_top5_cheapest_tours(), HTTP_200_OK)


@api_view(http_method_names=['GET'])
def tours_statistics_by_difficulty(request):
    return Response(
        Tour.report.get_group_statistics_by_difficulty(), HTTP_200_OK
    )