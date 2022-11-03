from rest_framework import permissions, request, response, status, views

from apps.common.permissions import IsAdmin, IsGuide, IsLeadGuide
from apps.natours import services
from apps.natours.api.v2.serializers.tours import (
    CreateTourSerializer,
    GetListTourSerializer,
    GetTourSerializer,
    UpdateTourSerializer,
)


class CreateUpdateTourView(views.APIView):
    permission_classes = [IsLeadGuide | IsGuide | IsAdmin]

    def post(self, request: request.Request) -> response.Response:
        serializer = CreateTourSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data, status.HTTP_201_CREATED)

    def put(self, request, **params):
        tour = services.natours.get_tour(params)
        serializer = UpdateTourSerializer(tour, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data, status.HTTP_200_OK)


class GetTourView(views.APIView):
    permissions_classes = (permissions.IsAuthenticated,)

    def get(self, request: request.Request, **params) -> response.Response:
        if any(params):
            tour = services.natours.get_complete_tour_info(params)
            serializer = GetTourSerializer(tour)
            return response.Response(serializer.data, status.HTTP_200_OK)


class GetAllTourView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request: request.Request) -> response.Response:
        serializer = GetListTourSerializer(
            services.natours.client_presentation_tours, many=True
        )
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class DeleteTourView(views.APIView):
    permissions_classes = IsAdmin | IsLeadGuide

    def delete(self, request, **params):
        services.natours.delete_tour(params)
        return response.Response(
            {"success": True, "message": "Delete tour was successful."},
            status.HTTP_204_NO_CONTENT,
        )
