from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.natours.models.locations import StartLocation, Locations
from apps.natours.models.tour import Tour
from apps.natours.models.tour_image import TourImage
from apps.users.api.v1.serializers import BaseUserSerializer
from apps.reviews.api.v1.serializers.tour_review import BaseTourReviewSerializer
from ..serializers.locations import LocationsSerializer, StartLocationSerializer

from ..serializers.tour_image import TourImageSerializer

User = get_user_model()


class CreateTourSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, )
    start_location = StartLocationSerializer(many=True, )
    locations = LocationsSerializer(many=True)

    class Meta:
        model = Tour
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        start_location = validated_data.pop('start_location', None)
        locations = validated_data.pop('locations', None)
        images = validated_data.pop('images', None)
        tour = Tour.objects.create(**validated_data)
        if start_location:
            start_location_points = [
                StartLocation(**obj, tour=tour) for obj in start_location
            ]
            tour.start_location.bulk_create(start_location_points)
        if locations:
            locations_points = [
                Locations(**obj) for obj in locations
            ]
            Locations.objects.bulk_create(locations_points, tour=tour)
        if images:
            tour_images = [
                TourImage(**obj, tour=tour) for obj in images
            ]
            TourImage.objects.bulk_create(tour_images)
        return tour


class GetAllTourSerializer(serializers.ModelSerializer):
    start_location = StartLocationSerializer(many=True, required=False)
    locations = LocationsSerializer(many=True, required=False)
    ratings_avg = serializers.DecimalField(
        max_digits=2,
        decimal_places=1,
        read_only=True
    )
    ratings_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tour
        exclude = ('secret_tour',)
        read_only_fields = (
            'id', 'name', 'price', 'summary', 'description',
            'discount_price', 'image_cover', 'duration', 'max_group_size',
            'difficulty', 'slug',
        )


class GetTourSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, required=False)
    start_location = StartLocationSerializer(many=True, required=False)
    locations = LocationsSerializer(many=True, required=False)
    reviews = BaseTourReviewSerializer(many=True, required=False)
    guides = BaseUserSerializer(many=True)
    ratings_avg = serializers.SerializerMethodField()
    ratings_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        exclude = ('secret_tour',)
        read_only_fields = (
            'id', 'name', 'price', 'summary', 'description', 'start_dates',
            'discount_price', 'image_cover', 'duration', 'max_group_size',
            'difficulty', 'start_location', 'images', 'locations', 'reviews'
        )

    def get_ratings_avg(self, tour):
        return tour.ratings_avg

    def get_ratings_quantity(self, tour):
        return tour.ratings_quantity


class UpdateTourSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, required=False)
    locations = LocationsSerializer(many=True, required=False)
    start_location = StartLocationSerializer(many=True, required=False)

    class Meta:
        model = Tour
        fields = '__all__'
        read_only_fields = ('id',)

    def update(self, tour, validated_data):
        images = validated_data.pop('images', None)
        locations = validated_data.pop('locations', None)
        start_location = validated_data.pop('start_location', None)
        for field in validated_data:
            tour.__dict__[field] = \
                validated_data.get(field, tour.__dict__[field])
        if images:
            tour.images.set(images)
        if locations:
            tour.locations.set(locations)
        if start_location:
            tour.start_location.set(start_location)
        return tour
