from rest_framework import serializers
from .models import *
from accounts.serializers import UserListSerializer


# DEPARTMENT SERIALIZERS

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name", "code")
        read_only_fields = fields


class DepartmentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


# COURSE SERIALIZERS

class CourseListSerializer(serializers.ModelSerializer):
    professor_details = UserListSerializer(source="professor", read_only=True)
    department_name = serializers.CharField(
        source="department.name", read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "code",
            #"department",
            "department_name",
            #"professor",
            "professor_details",
            "day_of_week",
            "start_time",
            "end_time",
            "capacity",
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    professor_details = UserListSerializer(source="professor", read_only=True)
    department_details = DepartmentListSerializer(
        source="department", read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


# For professor to view their courses
class ProfessorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "code", "day_of_week",
                  "start_time", "end_time")


# For student course list
class StudentCourseListSerializer(serializers.ModelSerializer):
    professor_details = UserListSerializer(source="professor", read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "code",
            "professor_details",
            "day_of_week",
            "start_time",
            "end_time",
            "credit_hours",
        )


# Student timetable
class StudentTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "day_of_week", "start_time", "end_time")


# ENROLLMENT SERIALIZER

class EnrollmentSerializer(serializers.ModelSerializer):
    student_details = UserListSerializer(source="student", read_only=True)
    course_details = CourseListSerializer(source="course", read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"


# MATERIAL SERIALIZERS

class MaterialSerializer(serializers.ModelSerializer):
    uploaded_by_details = UserListSerializer(
        source="uploaded_by", read_only=True)

    class Meta:
        model = Material
        fields = "__all__"


class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ("id", "title", "file", "created_at")


# ANNOUNCEMENT SERIALIZERS

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_details = UserListSerializer(
        source="created_by", read_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"


class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ("id", "title", "created_at")
