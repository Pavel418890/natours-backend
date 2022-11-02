from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers


class PointSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[
            MinValueValidator(-90.000000),
            MaxValueValidator(90.000000)
        ]
    )
    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[
            MinValueValidator(-180.000000),
            MaxValueValidator(180.000000)
        ]
    )
    name = serializers.CharField()


class LocationsSerializer(PointSerializer):
    day = serializers.IntegerField()


class StartLocationSerializer(PointSerializer):
    address = serializers.CharField()
