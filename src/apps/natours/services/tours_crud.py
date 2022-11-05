from typing import Iterable, Optional, Union

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Count, F, Manager, Prefetch 
from django.db.models.functions import Round
from django.utils.text import slugify

from ..models import Tour

User = get_user_model()

LookupField = dict[str, str | int]


class TourCRUDService:
    def get_multi_tours(
        self,
        filter: Optional[list] = None,
        order_by: Optional[Union[str, tuple, list, set]] = None,
    ) -> Manager:
        """
        Возвращает полную информацию турах для представления
        """
        tours = (
            Tour.objects.prefetch_related("locations", "start_locations", "start_dates")
            .only()
            .annotate(
                ratings_avg=Round(Avg(F("reviews__rating")), 2),
                ratings_quantity=Count("reviews__id"),
            )
        )
        if filter:
            if len(filter) > 1:
                tours = tours.filter(id__in=filter)
            else:
                tours = tours.get(id=filter[0])
        if order_by:
            if isinstance(order_by, str):
                tours = tours.order_by(order_by)
            tours = tours.order_by(*order_by)
        return tours

    @property
    def client_presentation_tours(self) -> list[Tour]:
        """
        Возвращает 9 наиболее популярных туров для представления пользователю
        """
        return self.get_multi_tours(order_by=("-ratings_quantity", "-ratings_avg"))[:9]

    def _get_lookup_fields(
        self,
        params: LookupField,
        lookup_keys: Optional[Iterable] = None,
    ) -> LookupField:
        if lookup_keys is None:
            lookup_keys = {"id", "pk", "slug"}
        return {field: params[field] for field in params if field in lookup_keys}

    def get_complete_tour_info(self, params: LookupField) -> Tour:
        """
        Возвращает полную инфорамацию о туре для представления пользователю
        """
        guides = Prefetch("guides", User.objects.select_related("profile"))
        lookup_fields = self._get_lookup_fields(params)
        queryset = (
            self.get_multi_tours()
            .prefetch_related(
                guides,
                "images",
            )
            .get(**lookup_fields)
        )
        return queryset

    def get_tour(self, params: LookupField) -> Tour:
        """
        Возвращает тур согласно переданному параметру
        """
        lookup_fields = self._get_lookup_fields(params)
        return Tour.objects.get(**lookup_fields)

    def create_new_tour(self, validated_data: dict) -> Tour:
        """
        Создает основной объект тура
        """
        name = validated_data.pop("name")
        new_tour = Tour.objects.create(
            name=name,
            slug=slugify(name),
            image_cover=validated_data.pop("image_cover"),
            price=validated_data.pop("price"),
            max_group_size=validated_data.pop("max_group_size"),
            difficulty=validated_data.pop("difficulty"),
            summary=validated_data.pop("summary"),
            description=validated_data.pop("description"),
            duration=validated_data.pop("duration"),
        )
        return new_tour

    @transaction.atomic
    def update_tour(self, tour: Tour, validated_data: dict):
        """
        Обновляет данные тура
        """
        name = validated_data.pop("name")
        if name and name != tour.name:
            tour.name = name
            tour.slug = slugify(name)
        tour.image_cover = validated_data.pop("image_cover", tour.image_cover)
        tour.price = validated_data.pop("price", tour.price)
        tour.difficulty = validated_data.pop("difficulty", tour.difficulty)
        tour.summary = validated_data.pop("summary", tour.summary)
        tour.description = validated_data.pop("description", tour.description)
        tour.duration = validated_data.pop("duration", tour.duration)
        tour.max_group_size = validated_data.pop("max_group_size", tour.max_group_size)
        tour.save()
        return tour

    @transaction.atomic
    def delete_tour(self, params: LookupField) -> None:
        """
        Удаляет тур согласно полученным параметрам
        """
        tour = self.get_tour(params)
        tour.delete()


natours = TourCRUDService()
