from django.contrib.auth import get_user_model
from django.db import connection
from django.db.models import Prefetch

from apps.bookings import models
from apps.natours.services import natours

User = get_user_model()


class BookingCustomerService:
    # def get_customer_bookings(self, customer: User) -> models.Booking:
    #     with connection.cursor() as c:
    #         result = c.execute(
    #             """
    #             WITH tour AS (SELECT t.id,
    #                                 t.name,
    #                                 t.slug,
    #                                 t.price,
    #                                 t.summary,
    #                                 t.duration,
    #                                 t.difficulty,
    #                                 t.image_cover,
    #                                 sd.start_date,
    #                                 t.max_group_size,
    #                                 COUNT(tr.review) AS review_quantity,
    #                                 ROUND(avg(tr.rating), 2) AS rating_avg
    #             FROM tours t

    #                 JOIN start_dates sd      ON t.id = sd.tour_id
    #                 JOIN start_locations sl  ON t.id = sl.tour_id
    #                 JOIN tour_reviews tr     ON t.id = tr.tour_id

    #             GROUP BY t.id,
    #                     t.name,
    #                     t.price,
    #                     t.summary,
    #                     t.duration,
    #                     t.difficulty,
    #                     t.image_cover,
    #                     t.max_group_size,
    #                     t.slug, sd.start_date)

    #             SELECT DISTINCT ON (created_at) created_at, tour, is_paid
    #             FROM bookings
    #                 JOIN tour   ON tour.id = bookings.tour_id

    #             WHERE user_id = %s AND is_paid;
    #             """,
    #             [customer.id]
    #         )
    #     return result.fetchall()

    def get_customer_bookings(self, customer: User):
        models.Booking.objects.prefetch_related(
            Prefetch("tour", queryset=natours.get_multi_tours())
        ).filter(user_id=customer.id, is_paid=True)


booking_customer = BookingCustomerService()
