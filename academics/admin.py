from django.contrib import admin
from .models import Department, Course, Enrollment, Material, Announcement


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "created_at",
        "updated_at",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "capacity",
        "department",
        "professor",
        "day_of_week",
        "start_time",
        "end_time",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "enrollment_status",
        "student",
        "course",
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "course",
        "uploaded_by",
        "created_at",
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course",
        "title",
        "created_by",
        "created_at",
    )
