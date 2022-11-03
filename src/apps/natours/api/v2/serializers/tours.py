from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from apps.natours import models, services
from apps.reviews.api.v1.serializers import BaseTourReviewSerializer
from apps.users.api.v1.serializers import BaseUserSerializer

from . import LocationsSerializer, StartLocationSerializer, TourImageSerializer

User = get_user_model()


__all__ = [
    "StartDatesSerializer",
    BaseTourSerializer,
    CreateTourSerializer,
    UpdateTourSerializer,
    GetListTourSerializer,
    GetTourSerializer,
]


class StartDatesSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()


class BaseTourSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    name = serializers.CharField()
    image_cover = serializers.ImageField()
    max_group_size = serializers.IntegerField()
    difficulty = serializers.ChoiceField(choices=models.Tour.DIFFICULTY_CHOICES)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    summary = serializers.CharField()
    description = serializers.CharField()
    secret_tour = serializers.BooleanField()
    duration = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        error_messages={"duration": "Max tour duration - one month."},
    )


class CreateTourSerializer(BaseTourSerializer):
    def create(self, validated_data):
        """
        Вызывает метод создания нового тура, после валидации данных запроса
        """
        return services.natours.create_new_tour(validated_data=validated_data)


class UpdateTourSerializer(BaseTourSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for fields_instance in fields.values():
            fields_instance.required = False
        return fields

    def update(self, tour, validated_data):
        """
        Вызывает метод обновления данных тура
        """
        return services.natours.update_tour(tour, validated_data)


class GetListTourSerializer(BaseTourSerializer):
    start_locations = StartLocationSerializer(many=True)
    locations = LocationsSerializer(many=True)
    start_dates = StartDatesSerializer(many=True)
    ratings_avg = serializers.DecimalField(
        max_digits=2, decimal_places=1, read_only=True
    )
    ratings_quantity = serializers.IntegerField(read_only=True)


class GetTourSerializer(GetListTourSerializer):
    images = TourImageSerializer(many=True, required=False)
    guides = BaseUserSerializer(many=True)
    reviews = BaseTourReviewSerializer(many=True, required=False)
