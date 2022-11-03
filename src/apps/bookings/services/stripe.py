import json

import stripe as s
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.natours.models import Tour

User = get_user_model()


class Stripe:
    s.api_key = settings.STRIPE_PRIVATE_KEY

    def get_tour_booking_checkout_session(self, user: User, tour_id: int) -> dict:
        tour = Tour.objects.get(id=tour_id)

        return s.checkout.Session.create(
            success_url="{}/bookings/".format(settings.CLIENT_BASE_URL),
            cancel_url="{}/failed/".format(settings.CLIENT_BASE_URL),
            customer_email=user.email,
            client_reference_id=tour.id,
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": tour.name,
                    "description": tour.summary,
                    "images": [
                        "{}/{}".format(settings.CLIENT_BASE_URL, tour.image_cover.url)
                    ],
                    "amount": int(tour.price * 100),
                    "currency": "usd",
                    "quantity": 1,
                }
            ],
        )

    def get_tour_booking_checkout_stage(
        self,
        payload: str,
        signature_header: str,
        webhook_secret_key=settings.STRIPE_WEBHOOK_SECRET_KEY,
    ) -> s.Event:

        event = None
        try:
            event = s.Webhook.construct_event(
                payload, signature_header, webhook_secret_key
            )
            return event
        except ValueError as e:
            # Invalid request body
            raise s.error.InvalidRequestError(e.args)

        except s.error.SignatureVerificationError as e:
            # Invalid signature
            raise e


stripe = Stripe()
