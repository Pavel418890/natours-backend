from typing import Dict, Generic, NoReturn, Optional, TypeVar

from django.utils.deconstruct import deconstructible
from rest_framework.serializers import ValidationError


def coordinates_validator(coordinates):
    """Проверяет координаты для Point типа моделей"""
    lat, lng = coordinates
    if lat < -90.000000 or lat > 90.000000 or lng < -180.000000 or lng > 180.000000:
        raise ValidationError("Invalid data for latitude/longitude")


@deconstructible
class FieldsPairEqualityValidator:
    """
    Проверяет уникальность двух значений для каждой пары объектов в коллекции
    """

    PairEqualityFields = TypeVar("PairEqualityFields")

    def __init__(
        self, fields: Generic[PairEqualityFields], message: Optional[str] = None
    ):
        self.fields = fields
        self.message = message

    def __call__(self, attrs: Dict[str, str]) -> NoReturn:
        error_message = (
            "Comparison fields must be in collection lists or tuples with len 2"
        )
        if not isinstance(self.fields, (list, tuple)):
            raise AttributeError(error_message)
        fields_set = set()
        pair_fields_count = 0
        for comparison_fields in self.fields:
            pair_fields_count += 1
            if len(comparison_fields) != 2:
                raise AttributeError(error_message)

            for field in comparison_fields:
                fields_set.add(attrs[field])
        if pair_fields_count % len(fields_set):
            raise ValidationError(self.message or error_message)
