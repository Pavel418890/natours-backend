from django.urls import path
from ..views.tour_review import (
    GetUpdateDeleteTourReviewView,
    GetAllReviewsOnTourView,
    CreateReviewOnTourView
)

urlpatterns = [
    path(
        'reviews/<int:tour_id>/',
        GetAllReviewsOnTourView.as_view(),
        name='tour-reviews'
    ),
    path(
        'tours/<int:tour_id>/review/',
        CreateReviewOnTourView.as_view(),
        name='new-tour-review'
    ),
    path(
        'review-detail/<int:review_id>/',
        GetUpdateDeleteTourReviewView.as_view(),
        name='review-detail'
    ),
]
