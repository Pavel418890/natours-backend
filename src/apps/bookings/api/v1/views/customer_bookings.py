from rest_framework import request, response, status, views

from apps.bookings.services.booking_customer_service import BookingCustomerService
from apps.common.permissions import IsUser

from ..serializers.booking_tour import TourBookingSerializer


class CustomerBookingsView(views.APIView):
    permission_classes = (IsUser,)

    booking_customer_service = BookingCustomerService()

    def get(self, request: request.Request) -> response.Response:

        customer = self.request.user
        books = self.booking_customer_service.get_customer_bookings(customer)
        serializer = TourBookingSerializer(books, many=True)
        return response.Response(serializer.data, status.HTTP_200_OK)
