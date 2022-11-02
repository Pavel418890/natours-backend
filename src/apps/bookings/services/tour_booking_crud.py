from django.db.transaction import atomic

from ..models import Booking
from apps.common.utils import Singleton
from apps.users.services.users_crud import UserCRUDService
from .stripe import Stripe
from stripe.api_resources.checkout.session import Session


class TourBookingCRUDService(metaclass=Singleton):

    booking_tour_manager = Booking.objects
    stripe = Stripe()

    @atomic
    def create_tour_booking(
        self, booking_tour_checkout_session: Session
    ) -> Booking:
        tour_id = booking_tour_checkout_session.client_reference_id
        user = UserCRUDService().get_user_by_email(
            email=booking_tour_checkout_session.customer_email
        )
        price = booking_tour_checkout_session.amount_subtotal / 100

        return self.booking_tour_manager.create(
            tour_id=tour_id,
            user=user,
            price=price,
        )
