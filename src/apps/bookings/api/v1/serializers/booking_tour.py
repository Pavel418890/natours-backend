from rest_framework import serializers

from apps.natours.api.v2.serializers.tours import GetListTourSerializer
from apps.users.api.v1.serializers.users import BaseUserSerializer


class TourBookingSerializer(serializers.Serializer):
    user = BaseUserSerializer()
    tour = GetListTourSerializer(required=False)
    tour_id = serializers.IntegerField()
    price = serializers.DecimalField(read_only=True, max_digits=7, decimal_places=2)
    is_paid = serializers.BooleanField()
