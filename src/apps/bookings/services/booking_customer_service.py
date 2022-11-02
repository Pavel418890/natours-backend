from django.contrib.auth import get_user_model

from apps.common.utils import Singleton
from ..models.booking_tours import Booking


User = get_user_model()


class BookingCustomerService(metaclass=Singleton):
    book_manager = Booking.objects

    def get_customer_bookings(self, customer: User) -> Booking:
        return self.book_manager.select_related('tour').filter(
            user=customer.id
        )


        


