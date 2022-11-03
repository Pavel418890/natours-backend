from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bookings.services.stripe import Stripe
from apps.common.permissions import IsUser


class StripeCheckoutSessionView(APIView):
    permission_classes = (IsUser,)

    stripe = Stripe()

    def get(self, request, tour_id):
        session = self.stripe.get_tour_booking_checkout_session(
            user=request.user, tour_id=tour_id
        )
        return Response(session)
