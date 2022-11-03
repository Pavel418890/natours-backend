from typing import Dict, Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from apps.services.image_thumbnail_creator import thumbnail_image
from apps.users.models import Profile, User


class ProfileCRUDService:
    def create_user_profile(
        self, user: User, data: Dict[str, Union[str, InMemoryUploadedFile]]
    ) -> Profile:
        """Создает профиль пользователя"""
        first_name = data.pop("first_name", None)
        last_name = data.pop("last_name", None)
        photo = data.pop("photo", None)
        return Profile.objects.create(
            user=user, first_name=first_name, last_name=last_name, photo=photo
        )

    def update_user_profile(
        self, user_profile: Profile, updated_fields: Dict[str, str]
    ) -> Profile:
        """
        Изменяет данные профиля пользователя, согласно переданным данным
        Возвращет пользователя с обновленными данными
        """
        user_profile.first_name = updated_fields.get(
            "first_name", user_profile.first_name
        )
        user_profile.last_name = updated_fields.get("last_name", user_profile.last_name)
        user_profile.save()
        return user_profile

    @transaction.atomic
    def update_user_photo(
        self, user_profile: Profile, received_from_user_image: InMemoryUploadedFile
    ) -> Profile:
        """
        Вызывает создание миниатурного изображения для
        загруженного пользователем файла.
        Возвращает профиль с обновленным изображением
        """
        resized_image = thumbnail_image(128, 128, received_from_user_image)
        user_profile.photo.save(
            name=received_from_user_image.name,
            content=resized_image,
            save=False,
        )
        user_profile.save()
        profile = user_profile
        return profile


profile = ProfileCRUDService()
