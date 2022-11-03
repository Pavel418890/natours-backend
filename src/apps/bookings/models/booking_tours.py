from django.db import models

from apps.natours.models import Tour
from apps.users.models import User


class Booking(models.Model):
    tour = models.ForeignKey(
        verbose_name="Booking belong to the tour",
        to=Tour,
        related_name="bookings",
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        verbose_name="Booking belong to the user",
        to=User,
        related_name="bookings",
        on_delete=models.DO_NOTHING,
    )
    price = models.DecimalField(
        verbose_name="Booking price",
        max_digits=7,
        decimal_places=2,
    )
    created_at = models.DateTimeField(
        verbose_name="Booking creation datetime",
        auto_now_add=True,
    )
    is_paid = models.BooleanField(verbose_name="Booking payment status", default=True)

    class Meta:
        db_table = "bookings"
