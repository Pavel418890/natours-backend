from rest_framework import serializers


class PointSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    coordinates = serializers.ListField()
    description = serializers.CharField()


class LocationsSerializer(PointSerializer):
    day = serializers.IntegerField()


class StartLocationSerializer(PointSerializer):
    address = serializers.CharField()
