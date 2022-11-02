from rest_framework import serializers

from apps.users.api.v1.serializers import BaseUserSerializer
from apps.natours.api.v2.serializers.tours import BaseTourSerializer


class TourBookingSerializer(serializers.Serializer):
    user = BaseUserSerializer()
    tour = BaseTourSerializer(required=False)
    tour_id = serializers.IntegerField()
    price = serializers.DecimalField(
        read_only=True, max_digits=7, decimal_places=2
    )



