from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_402_PAYMENT_REQUIRED
from rest_framework.views import APIView

from apps.bookings import services

from ..serializers.booking_tour import TourBookingSerializer


class BookTourView(APIView):
    def post(self, request: Request) -> Response:
        tour_booking_checkout_event = services.stripe.get_tour_booking_checkout_stage(
            payload=request.body, signature_header=request.META["HTTP_STRIPE_SIGNATURE"]
        )
        tour_booking_session_data = tour_booking_checkout_event.data.object
        if tour_booking_checkout_event.type == "checkout.session.completed":
            booked_tour = services.tour_booking.create_tour_booking(
                tour_booking_session_data
            )
            serializer = TourBookingSerializer(booked_tour)
            return Response(data=serializer.data, status=HTTP_201_CREATED)

        else:
            failed_book = services.tour_booking.create_failed_booking(
                tour_booking_session_data
            )
            serializer = TourBookingSerializer(failed_book)
            return Response(data=serializer.data, status=HTTP_402_PAYMENT_REQUIRED)
