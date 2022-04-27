from rest_framework import serializers


class BaseReviewSerializer(serializers.Serializer):
    """Abstract"""
    id = serializers.IntegerField(read_only=True)
    review = serializers.CharField(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class GetAllReviews(BaseReviewSerializer):
    """Класс администрирования отзывов"""
    def validate(self, data):
        NotImplemented('In future.')


