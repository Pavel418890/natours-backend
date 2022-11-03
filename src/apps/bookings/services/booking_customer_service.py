from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from apps.bookings import models
from apps.natours.services import natours

User = get_user_model()


class BookingCustomerService:
    def get_customer_bookings(self, customer: User) -> Optional[list[models.Booking]]:
        return models.Booking.objects.prefetch_related(
            Prefetch("tour", queryset=natours.get_multi_tours())
        ).filter(user_id=customer.id, is_paid=True)


booking_customer = BookingCustomerService()
