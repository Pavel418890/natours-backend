from django.db.transaction import atomic
from stripe.api_resources.checkout.session import Session

from apps.bookings.services import stripe
from apps.users import services

from ..models import Booking


class TourBookingCRUDService:
    def _get_data_from_stripe_session(self, stirpe_session: Session) -> Booking:
        tour_id = stirpe_session.client_reference_id
        user = services.user.get_user_by_email(stirpe_session.customer_email)
        price = stirpe_session.amount_subtotal / 100
        return Booking(tour_id=tour_id, user=user, price=price, is_paid=False)

    @atomic
    def create_tour_booking(self, stirpe_session: Session) -> Booking:
        book = self._get_data_from_stripe_session(stirpe_session)
        book.is_paid = True
        book.save()
        return book

    @atomic
    def create_failed_booking(self, stripe_session: Session) -> Booking:
        book = self._get_data_from_stripe_session(stripe_session)
        book.is_paid = False
        book.save()
        return book


tour_booking = TourBookingCRUDService()
