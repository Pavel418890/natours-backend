from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class User(AbstractBaseUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    ADMIN = "admin"
    USER = "user"
    LEAD_GUIDE = "lead_guide"
    GUIDE = "guide"
    USER_ROLE_CHOICES = (
        (ADMIN, "admin"),
        (USER, "user"),
        (GUIDE, "guide"),
        (LEAD_GUIDE, "lead_guide"),
    )

    objects = BaseUserManager()
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        verbose_name="User Role",
        max_length=15,
        default="user",
        choices=USER_ROLE_CHOICES,
    )
    created_at = models.DateTimeField(
        verbose_name="User Created At",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="User Updated At",
        auto_now=True,
    )
    is_active = models.BooleanField(verbose_name="Status User", default=True)
    is_email_confirmed = models.BooleanField(
        verbose_name="User Email Address Confirmation Status",
        default=False,
    )
    password_reset_token = models.CharField(
        verbose_name="Reset User Password From Token", max_length=255, null=True
    )
    password_changed_at = models.DateTimeField(
        verbose_name="Last Changed Password Datetime", null=True
    )

    class Meta:
        db_table = "users"
        app_label = "users"

    def __str__(self):
        return f"{self.email} - {self.role}"
