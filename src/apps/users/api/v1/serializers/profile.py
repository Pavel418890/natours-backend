from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from apps.users import services
from apps.users.models import Profile

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(allow_null=True, required=False)
    last_name = serializers.CharField(allow_null=True, required=False)
    photo = serializers.ImageField(read_only=True, use_url=True)


class UpdateUserProfilePhotoSerializer(ProfileSerializer):
    photo = serializers.ImageField()

    def update(
        self, profile: Profile, validated_data: dict[str, InMemoryUploadedFile]
    ) -> Profile:
        received_photo = validated_data.pop('photo')
        return services.profile.update_user_photo(profile, received_photo)


class UpdateUserProfileSerializer(ProfileSerializer):
    def update(
        self, profile: Profile, validated_data: dict[str, str]
    ) -> Profile:
        return services.profile.update_user_profile(profile, validated_data)
