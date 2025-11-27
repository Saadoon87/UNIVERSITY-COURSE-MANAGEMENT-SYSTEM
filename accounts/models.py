from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PROFESSOR = "PROFESSOR", "Professor"
        STUDENT = "STUDENT", "Student"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    national_id = models.CharField(max_length=14)

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT
    )

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # students only
    academic_year = models.IntegerField(null=True, blank=True)

    # Auto-generated email
    university_email = models.EmailField(unique=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Auto-generate university email
        if not self.university_email:
            prefix = "student" if self.role == "STUDENT" else "prof"
            self.university_email = (
                f"{self.first_name.lower()}."
                f"{self.last_name.lower()}."
                f"{self.national_id[-4:]}@{prefix}.university.com"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
