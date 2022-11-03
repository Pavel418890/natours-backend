from django.urls import include, path

from ..views.booking_tours import BookTourView
from ..views.customer_bookings import CustomerBookingsView
from ..views.stripe_checkout_session import StripeCheckoutSessionView

urlpatterns = [
    path(
        "bookings/<int:tour_id>/",
        StripeCheckoutSessionView.as_view(),
        name="create-booking-tour-checkout",
    ),
    path("bookings/tour-booking/", BookTourView.as_view(), name="book-tour"),
    path("bookings/my/", CustomerBookingsView.as_view(), name="user-bookings"),
]
