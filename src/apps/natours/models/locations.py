from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.natours.models.tour import Tour


class Point(models.Model):
    latitude = models.DecimalField(
        verbose_name='The Tour Longitude coordinates',
        max_digits=10,
        decimal_places=6,
        validators=[
            MinValueValidator(-90.000000),
            MaxValueValidator(90.000000)
        ]
    )
    longitude = models.DecimalField(
        verbose_name='The Tour Longitude coordinates',
        max_digits=10,
        decimal_places=6,
        validators=[
            MinValueValidator(-180.000000),
            MaxValueValidator(180.000000)
        ]
    )
    name = models.CharField(
        verbose_name='The Tour Point Name',
        max_length=500,
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        managed = False


class StartLocation(Point):
    address = models.CharField(
        verbose_name='The Starting Point Address',
        max_length=255,
    )
    tour = models.ForeignKey(
        to=Tour,
        on_delete=models.CASCADE,
        related_name='start_locations'
    )

    def __str__(self):
        return self.address

    class Meta:
        db_table = 'start_locations'


class Locations(Point):
    day = models.IntegerField(
        verbose_name='The Tour Point Day',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31)
        ],
        error_messages={'day': 'Max tour duration - one month'}
    )
    tour = models.ForeignKey(
        to=Tour,
        on_delete=models.CASCADE,
        related_name='locations'
    )

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return 'Day: {} {}'.format(self.day, self.name)