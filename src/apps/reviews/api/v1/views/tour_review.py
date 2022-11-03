from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsOwner, IsUser
from apps.reviews import services
from apps.reviews.api.v1 import serializers


class GetAllReviewsOnTourView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, tour_id: int) -> Response:
        """
        Возвращает основную информации по всем отзывам на
        конкретный тур, после валидации объектов запроса
        """
        count, reviews = services.tour_reviews.get_all_reviews_on_tour(tour_id)
        serializer = serializers.BaseTourReviewSerializer(reviews, many=True)
        return Response(
            data={"result": count, "data": serializer.data}, status=HTTP_200_OK
        )


class GetUpdateDeleteTourReviewView(APIView):
    permission_classes = [IsOwner | IsAdmin]

    def get(self, request: Request, review_id: int) -> Response:
        """
        Запрос на получение деталей отзыва после валидации объектов запроса
        """
        review = services.tour_reviews.get_tour_review_by_id(review_id=review_id)
        serializer = serializers.BaseTourReviewSerializer(review)
        return Response(serializer.data, HTTP_200_OK)

    def put(self, request: Request, review_id) -> Response:
        """
        Вызов метода поиска отзыва на тур согласно переданному идентификатору
        """
        review = services.tour_reviews.get_tour_review_by_id(review_id=review_id)
        serializer = serializers.UpdateReviewOnTourSerializer(review, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)

    def delete(self, request: Request, review_id: int) -> Response:
        """
        Вызывает метод удаления отзыва на тур
        """
        services.tour_reviews.delete_review_on_tour(review_id)
        return Response(
            {"status": "Success", "detail": "Review was deleted"}, HTTP_204_NO_CONTENT
        )


class CreateReviewOnTourView(APIView):
    permission_classes = [IsUser]

    def post(self, request: Request, tour_id: int) -> Response:
        """
        Вызывает метод создания отзыва на тур после валидации объектов запроса
        """
        serializer = serializers.CreateReviewOnTourSerializer(
            data={"user_id": self.request.user.id, "tour_id": tour_id, **request.data}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)
