from io import BytesIO
from typing import Union

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import \
    InMemoryUploadedFile, TemporaryUploadedFile


def thumbnail_image(
        required_image_width: int,
        required_image_height: int,
        image_file: Union[InMemoryUploadedFile, TemporaryUploadedFile],
        saving_format: str = 'JPEG'
) -> ContentFile:
    with Image.open(image_file) as img:
        img.thumbnail((required_image_width, required_image_height))
        bytes_image_buffer = BytesIO()
        img.save(bytes_image_buffer, format='webp')
        return ContentFile(bytes_image_buffer.getvalue())


