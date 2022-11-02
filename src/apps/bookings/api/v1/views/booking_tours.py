from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_201_CREATED, HTTP_402_PAYMENT_REQUIRED
from rest_framework.views import APIView

from apps.bookings.services.stripe import Stripe
from apps.bookings.services.tour_booking_crud import TourBookingCRUDService
from ..serializers.booking_tour import TourBookingSerializer


class BookTourView(APIView):
    stripe = Stripe()
    tour_booking = TourBookingCRUDService()

    def post(self, request: Request) -> Response:
        tour_booking_checkout_event =\
            self.stripe.get_tour_booking_checkout_stage(
                payload=request.body,
                signature_header=request.META['HTTP_STRIPE_SIGNATURE']
            )
        tour_booking_session_data = tour_booking_checkout_event.data.object
        if tour_booking_checkout_event.type == 'checkout.session.completed':
            booked_tour = self.tour_booking.create_tour_booking(
                tour_booking_session_data
            )
            serializer = TourBookingSerializer(booked_tour)
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        else:
            return Response({}, status=HTTP_402_PAYMENT_REQUIRED)
