from rest_framework import request, response, status, views

from apps.common.permissions import IsUser

from ..serializers.booking_tour import TourBookingSerializer
from apps.bookings.services import booking_customer

class CustomerBookingsView(views.APIView):
    permission_classes = (IsUser,)

    def get(self, request: request.Request) -> response.Response:

        customer = self.request.user
        books = booking_customer.get_customer_bookings(customer)
        print(books)
        serializer = TourBookingSerializer(books, many=True)
        print(serializer.data)
        return response.Response(serializer.data, status.HTTP_200_OK)
