from typing import Optional, TypedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.reviews import models, services
from apps.reviews.api.v1.serializers.base_review import BaseReviewSerializer
from apps.users.api.v1.serializers import SignedUser
from apps.users.api.v1.serializers.users import BaseUserSerializer


class TourReviewType(TypedDict):
    id: int
    review: Optional[str]
    rating: Optional[int]
    user: SignedUser
    tour_id: int


class BaseTourReviewSerializer(BaseReviewSerializer):
    user = BaseUserSerializer(read_only=True)
    tour_id = serializers.IntegerField(read_only=True)


class CreateReviewOnTourSerializer(BaseReviewSerializer):
    review = serializers.CharField()
    rating = serializers.IntegerField()
    user = BaseUserSerializer(read_only=True)
    tour_id = serializers.IntegerField()
    user_id = serializers.IntegerField(write_only=True)

    def create(self, validation_data: TourReviewType) -> models.TourReview:
        """
        Вызывает функцию создания нового отзыва на тур
        Возвращает данный отзыв
        """
        new_review = services.tour_reviews.create_tour_review(validation_data)
        return new_review


class UpdateReviewOnTourSerializer(BaseReviewSerializer):
    review = serializers.CharField(required=False)
    rating = serializers.IntegerField(required=False)

    def validate(self, request_data: TourReviewType) -> TourReviewType:
        """Проверяет, что хотя бы один аттрибут отзыва был изменен"""
        if not any(
            (
                request_data.get("review"),
                request_data.get("rating"),
            )
        ):
            raise ValidationError("Content must be edited for updating review")
        return request_data

    def update(
        self, review: models.TourReview, validated_data: dict[str, int | TourReviewType]
    ) -> models.TourReview:
        """
        Вызывает метод изменения отзыва пользователя
        Возвращает данный отзыв
        """
        return services.tour_reviews.update_tour_review(review, validated_data)
