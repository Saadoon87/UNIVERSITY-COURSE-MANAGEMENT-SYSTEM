from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    ordering = ("id",)
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "national_id",
        "role",
        "department",
        "academic_year",
        "university_email",
        "is_staff",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "national_id",
                "role",
                "department",
                "academic_year",
                "university_email",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "national_id",
                "role",
                "department",
                "academic_year",
            ),
        }),
    )

    search_fields = ("email", "first_name", "last_name")
