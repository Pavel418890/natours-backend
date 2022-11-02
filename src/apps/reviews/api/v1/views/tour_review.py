from rest_framework.views import APIView
from rest_framework.status import \
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from apps.common.permissions import IsAdmin, IsUser, IsOwner
from apps.reviews.services.tour_reviews_crud import TourReviewCRUDService
from ..serializers.tour_review import (
    BaseTourReviewSerializer,
    CreateReviewOnTourSerializer,
    UpdateReviewOnTourSerializer,
)


class GetAllReviewsOnTourView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, tour_id: int) -> Response:
        """
        Возвращает основную информации по всем отзывам на 
        конкретный тур, после валидации объектов запроса
        """
        reviews_quantity, reviews = \
            TourReviewCRUDService().get_all_reviews_on_tour(tour_id)
        serializer = BaseTourReviewSerializer(reviews, many=True)
        return Response(
            data={'result': reviews_quantity, 'data': serializer.data},
            status=HTTP_200_OK
        )


class GetUpdateDeleteTourReviewView(APIView):
    permission_classes = [IsOwner | IsAdmin]

    reviews_crud = TourReviewCRUDService()

    def get(self, request: Request, review_id: int) -> Response:
        """
        Запрос на получение деталей отзыва после валидации объектов запроса
        """
        review = self.reviews_crud.get_tour_review_by_id(review_id=review_id)
        serializer = BaseTourReviewSerializer(review)
        return Response(serializer.data, HTTP_200_OK)

    def put(self, request: Request, review_id) -> Response:
        """
        Вызов метода поиска отзыва на тур согласно переданному идентификатору
        """
        review = self.reviews_crud.get_tour_review_by_id(review_id=review_id)
        serializer = UpdateReviewOnTourSerializer(review, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)

    def delete(self, request: Request, review_id: int) -> Response:
        """
        Вызывает метод удаления отзыва на тур
        """
        self.reviews_crud.delete_review_on_tour(review_id)
        return Response(
            {'status': 'Success', 'detail': 'Review was deleted'},
            HTTP_204_NO_CONTENT
        )


class CreateReviewOnTourView(APIView):
    permission_classes = [IsUser]

    def post(self, request: Request, tour_id: int) -> Response:
        """
        Вызывает метод создания отзыва на тур после валидации объектов запроса
        """
        serializer = CreateReviewOnTourSerializer(data={
            'user_id': self.request.user.id,
            'tour_id': tour_id,
            **request.data
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)
