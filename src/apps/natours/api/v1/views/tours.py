from django.http import HttpResponseBadRequest, JsonResponse

from rest_framework import generics, views, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.common.mixins import MultipleFieldLookupMixin
from apps.common.permissions import IsAdmin, IsGuide, IsLeadGuide, IsUser
from ..serializers.tours import (
    CreateTourSerializer,
    UpdateTourSerializer,
    GetAllTourSerializer,
    GetTourSerializer
)
from apps.natours.models import Tour


class CreateTourView(generics.CreateAPIView):
    permission_classes = [IsLeadGuide | IsGuide | IsAdmin]
    queryset = Tour.objects.filter(secret_tour=False)
    serializer_class = CreateTourSerializer


class GetAllTourView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Tour.objects.filter(secret_tour=False)
    serializer_class = GetAllTourSerializer


class GetTourView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    permission_classes = [IsUser | IsAdmin]
    queryset = Tour.objects.filter(secret_tour=False)
    serializer_class = GetTourSerializer
    lookup_fields = ['pk', 'slug']


class UpdateDeleteTour(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsLeadGuide | IsAdmin]
    queryset = Tour.objects.all()
    serializer_class = UpdateTourSerializer


class ToursToMonthAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        report = Tour.report.tours_to_month(year)
        return Response(report, status.HTTP_200_OK)


class TourStatisticsAPIView(views.APIView):
    permission_classes = [IsAdmin | IsLeadGuide]

    def get(self, request, *args, **kwargs):
        report = Tour.report.tour_statistics()

        return Response(data=report, status=status.HTTP_200_OK)


class Top5CheapTourAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            return Response(
                data=Tour.report.top_5_cheap(), status=status.HTTP_200_OK
            )
        return HttpResponseBadRequest('Something went wrong')
