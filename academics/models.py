from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Course(models.Model):
    class Days(models.TextChoices):
        SUNDAY = "SUNDAY", "Sunday"
        MONDAY = "MONDAY", "Monday"
        TUESDAY = "TUESDAY", "Tuesday"
        WEDNESDAY = "WEDNESDAY", "Wednesday"
        THURSDAY = "THURSDAY", "Thursday"
        FRIDAY = "FRIDAY", "Friday"
        SATURDAY = "SATURDAY", "Saturday"

    name = models.CharField(max_length=125)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    credit_hours = models.IntegerField()
    capacity = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    professor = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "PROFESSOR"},
    )
    day_of_week = models.CharField(choices=Days.choices, max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ENROLLED = "ENROLLED", "Enrolled"
        DROPPED = "DROPPED", "Dropped"

    student = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        limit_choices_to={"role": "STUDENT"},
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    enrollment_status = models.CharField(
        choices=Status.choices,
        max_length=10,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"], name="unique_enrollment"
            )
        ]

    def __str__(self):
        return f"{self.student.email} → {self.course.code}"


class Material(models.Model):

    def material_upload_path(instance, filename):
        return f"materials/{instance.course.department.name}/{instance.course.code}/{filename}"

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "PROFESSOR"},
    )

    title = models.CharField(max_length=125)
    file = models.FileField(upload_to=material_upload_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "PROFESSOR"},
    )
    title = models.CharField(max_length=125)
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"
