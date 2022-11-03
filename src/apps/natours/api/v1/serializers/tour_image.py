from rest_framework import serializers


class TourImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
