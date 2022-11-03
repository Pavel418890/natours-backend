# Generated by Django 4.0.2 on 2022-02-23 11:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email Address"
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "admin"),
                            ("user", "user"),
                            ("guide", "guide"),
                            ("lead_guide", "lead_guide"),
                        ],
                        default="user",
                        max_length=15,
                        verbose_name="User Role",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="User Created At"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="User Updated At"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Status User"),
                ),
                (
                    "is_email_confirmed",
                    models.BooleanField(
                        default=False,
                        verbose_name="User Email Address Confirmation Status",
                    ),
                ),
                (
                    "password_reset_token",
                    models.CharField(
                        max_length=255,
                        null=True,
                        verbose_name="Reset User Password From Token",
                    ),
                ),
                (
                    "password_changed_at",
                    models.DateTimeField(
                        null=True, verbose_name="Last Changed Password Datetime"
                    ),
                ),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=255, null=True, verbose_name="User First Name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=255, null=True, verbose_name="User Last Name"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        default="default.jpg",
                        null=True,
                        upload_to="",
                        verbose_name="User Profile Photo",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User Account Info",
                    ),
                ),
            ],
            options={
                "db_table": "profiles",
            },
        ),
    ]
