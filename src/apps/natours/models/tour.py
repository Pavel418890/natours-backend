from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from .tour_report import Report

User = get_user_model()


class Tour(models.Model):
    EASY = "easy"
    MEDIUM = "medium"
    DIFFICULT = "difficult"
    DIFFICULTY_CHOICES = (
        (EASY, "easy"),
        (MEDIUM, "medium"),
        (DIFFICULT, "difficult")
    )

    objects = models.Manager()
    report = Report()

    slug = models.SlugField(null=True, db_index=True, unique=True)
    name = models.CharField(
        verbose_name="Tour Name", max_length=200
    )
    image_cover = models.ImageField(
        verbose_name="Tour Main Image",
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name='Tour Duration',
        default=1,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(31)
        ],
        error_messages={'duration': 'Max tour duration - one month.'}
    )
    max_group_size = models.PositiveSmallIntegerField(
        verbose_name='Max Group Size',
        default=5,
    )
    difficulty = models.CharField(
        verbose_name='Tour Difficulty',
        choices=DIFFICULTY_CHOICES,
        max_length=10,
        default=EASY,
    )
    price = models.DecimalField(
        verbose_name='Tour Price',
        max_digits=7,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name='Discount Tour Price',
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    summary = models.TextField(null=True, verbose_name='Tour Summary')
    description = models.TextField(
        null=True, blank=True, verbose_name='Tour Description'
    )
    secret_tour = models.BooleanField(
        verbose_name='Tour Creation Status(False if tour registration is done)',
        default=True
    )
    guides = models.ManyToManyField(
        verbose_name='Tour Guides',
        to=User,
        related_name='tours',
    )

    def __str__(self):
        return f'{self.name} {self.price}'

    class Meta:
        db_table = 'tours'
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_discount_price_lte_general_price",
                check=models.Q(price__gt=models.F("discount_price"))
            ),
        ]


class TourStartDates(models.Model):
    start_date = models.DateTimeField(
        verbose_name='Tour start date',
    )
    tour = models.ForeignKey(Tour, models.CASCADE, related_name='start_dates')

    class Meta:
        db_table = 'start_dates'

    def __str__(self):
        return str(self.start_date)

