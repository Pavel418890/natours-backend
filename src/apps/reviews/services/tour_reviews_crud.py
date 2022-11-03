from typing import Union

from django.contrib.auth import get_user_model

from apps.reviews.models.tour_review import TourReview

User = get_user_model()


class TourReviewCRUDService:
    def get_all_reviews_on_tour(self, tour_id: int) -> tuple[int, list[TourReview]]:
        """Возвращает все отзывы на тур"""
        reviews = TourReview.objects.select_related("user__profile", "tour").filter(
            tour_id=tour_id
        )
        reviews_quantity = reviews.count()
        return reviews_quantity, reviews

    def get_tour_review_by_id(self, review_id: int) -> TourReview:
        """Возвращает отзыв по индентификатору"""
        return TourReview.objects.select_related("user__profile", "tour").get(
            pk=review_id
        )

    def create_tour_review(self, review_data: dict[str, Union[str, int]]) -> TourReview:
        """Создает в БД новый отзыв на тур и возвращает его"""
        return TourReview.objects.create(**review_data)

    def update_tour_review(
        self, review_to_update, new_data: dict[str, Union[str, int]]
    ) -> TourReview:
        """Обновляет данные тура и возвращает его"""
        for field in new_data:
            review_to_update.__dict__[field] = new_data[field]
        review_to_update.save()
        return review_to_update

    def delete_review_on_tour(self, review_id: int) -> None:
        self.get_tour_review_by_id(review_id).delete()


tour_reviews = TourReviewCRUDService()
