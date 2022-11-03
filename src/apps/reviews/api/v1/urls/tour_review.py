from django.urls import path

from apps.reviews.api.v1.views import tour_review

urlpatterns = [
    path(
        "reviews/<int:tour_id>/",
        tour_review.GetAllReviewsOnTourView.as_view(),
        name="tour-reviews",
    ),
    path(
        "tours/<int:tour_id>/review/",
        tour_review.CreateReviewOnTourView.as_view(),
        name="new-tour-review",
    ),
    path(
        "review-detail/<int:review_id>/",
        tour_review.GetUpdateDeleteTourReviewView.as_view(),
        name="review-detail",
    ),
]
