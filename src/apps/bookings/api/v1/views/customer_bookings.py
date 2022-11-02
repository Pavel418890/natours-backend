from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.common.permissions import IsUser
from apps.bookings.services.booking_customer_service import BookingCustomerService
from ..serializers.booking_tour import TourBookingSerializer


class CustomerBookingsView(APIView):
    permission_classes = (IsUser, )

    booking_customer_service = BookingCustomerService()
    
    def get(self, request: Request) -> Response:
        customer = self.request.user
        books = self.booking_customer_service.get_customer_bookings(customer)
        serializer = TourBookingSerializer(books, many=True)
        return Response(serializer.data, HTTP_200_OK)
