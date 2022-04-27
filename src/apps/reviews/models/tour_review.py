from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

from django.core.validators import MinValueValidator, MaxValueValidator
from apps.natours.models import Tour
User = get_user_model()


class TourReview(models.Model):
    review = models.TextField(verbose_name='Review Content')
    rating = models.IntegerField(
            verbose_name='Review Rating',
            validators=[MinValueValidator(1), MaxValueValidator(5)],
            default=3
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tour = models.ForeignKey(
        verbose_name='Tour Review',
        related_name='reviews',
        to=Tour,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='User Review To Tour',
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        db_table = 'tour_reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['tour', 'user'],
                name='unique_review',
            ),
        ]

    def __str__(self):
        return f'{self.review} {self.rating}'
