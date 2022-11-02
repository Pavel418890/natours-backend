from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsGuide, IsLeadGuide, IsUser
from apps.natours.services.tours_crud import TourCRUDService, Tour
from ..serializers.tours import (
    GetAllTourSerializer,
    GetTourSerializer,
    CreateTourSerializer,
    UpdateTourSerializer
)

TourCRUDService = TourCRUDService()


class CreateUpdateTourView(APIView):
    permission_classes = [IsLeadGuide | IsGuide | IsAdmin]

    def post(self, request: Request) -> Response:
        serializer = CreateTourSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, HTTP_201_CREATED)

    def put(self, request, **params):
        tour = TourCRUDService.get_tour(params)
        serializer = UpdateTourSerializer(tour, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, HTTP_200_OK)


class GetTourView(APIView):
    permissions_classes = (IsAuthenticated,)

    def get(self, request: Request, **params) -> Response:
        if any(params):
            tour = TourCRUDService.get_complete_tour_info(params)
            serializer = GetTourSerializer(tour)
            return Response(serializer.data, HTTP_200_OK)


class GetAllTourView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        serializer = GetAllTourSerializer(
            TourCRUDService.client_presentation_tours, many=True
        )
        return Response(serializer.data, status=HTTP_200_OK)


class DeleteTourView(APIView):
    permissions_classes = (IsAdmin | IsLeadGuide)

    def delete(self, request, **params):
        TourCRUDService.delete_tour(params)
        return Response(
            {'success': True, 'message': 'Delete tour was successful.'},
            HTTP_204_NO_CONTENT
        )
