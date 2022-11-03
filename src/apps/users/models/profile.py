from django.db import models

from .user import User


class Profile(models.Model):
    user = models.OneToOneField(
        verbose_name="User Account Info", to=User, on_delete=models.CASCADE
    )
    first_name = models.CharField(
        verbose_name="User First Name", max_length=255, null=True
    )
    last_name = models.CharField(
        verbose_name="User Last Name", max_length=255, null=True
    )
    photo = models.ImageField(
        verbose_name="User Profile Photo",
        default="default.jpg",
    )

    class Meta:
        db_table = "profiles"
