from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "email", "password", "confirm_password",
            "first_name", "last_name", "national_id",
            "role", "department", "academic_year"
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )

        role = attrs.get("role")
        department = attrs.get("department")
        academic_year = attrs.get("academic_year")

        # STUDENT RULES
        if role == "STUDENT":
            if not department:
                raise serializers.ValidationError(
                    {"department": "Department is required for students"}
                )
            if not academic_year:
                raise serializers.ValidationError(
                    {"academic_year": "Academic Year is required for students"}
                )

        # PROFESSOR RULES
        if role == "PROFESSOR":
            if not department:
                raise serializers.ValidationError(
                    {"department": "Department is required for professors"}
                )
            if academic_year:
                raise serializers.ValidationError(
                    {"academic_year": "Academic Year is not allowed for professors"}
                )

        # ADMIN RULES
        if role == "ADMIN":
            if department:
                raise serializers.ValidationError(
                    {"department": "Admins cannot belong to a department"}
                )
            if academic_year:
                raise serializers.ValidationError(
                    {"academic_year": "Admins cannot have academic year"}
                )

        return attrs

    def create(self, validated_data):

        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            national_id=validated_data["national_id"],
            role=validated_data["role"],
            department=validated_data.get("department", None),
            academic_year=validated_data.get("academic_year", None),
        )

        return user


class UserListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name", read_only=True)
    department_code = serializers.CharField(
        source="department.code", read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "department_name",
            "department_code"
        )


class UserDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name", read_only=True)
    department_code = serializers.CharField(
        source="department.code", read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "department",
            "department_name",
            "department_code",
            "academic_year",
            "university_email"
        )
