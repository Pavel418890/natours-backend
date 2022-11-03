from django.conf import settings
from django.db import models

from .tour import Tour


class TourImage(models.Model):
    image = models.ImageField()
    tour = models.ForeignKey(
        to=Tour, null=True, on_delete=models.CASCADE, related_name="images"
    )

    class Meta:
        db_table = "tour_images"

    def __str__(self):
        return f"{self.image.url}"
