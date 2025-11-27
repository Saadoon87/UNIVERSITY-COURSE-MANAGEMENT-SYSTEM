from rest_framework import generics, permissions, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


# ROLE PERMISSIONS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "PROFESSOR"


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "STUDENT"


#  DEPARTMENT VIEWS

class ShowAllDepartmentsView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterDepartmentView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer
    permission_classes = [IsAdmin]


# COURSE VIEWS

class ShowAllCoursesView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterCourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAdmin]


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateCourseView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAdmin]


class DeleteCourseView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAdmin]


#  PROFESSOR VIEWS

class ProfessorCoursesView(generics.ListAPIView):
    serializer_class = ProfessorCourseSerializer
    permission_classes = [IsProfessor]

    def get_queryset(self):
        return Course.objects.filter(professor=self.request.user)


class ProfessorCourseStudentsView(APIView):
    permission_classes = [IsProfessor]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id, professor=request.user)
        except Course.DoesNotExist:
            return Response({"error": "Not allowed"}, status=403)

        enrollments = Enrollment.objects.filter(
            course=course, enrollment_status="ENROLLED")
        data = [
            {
                "student_id": e.student.id,
                "student_name": f"{e.student.first_name} {e.student.last_name}",
                "university_email": e.student.university_email,
                "academic_year": e.student.academic_year
            }
            for e in enrollments
        ]
        return Response(data, status=200)


#  ENROLLMENT (STUDENTS)

class EnrollInCourseView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, course_id):
        user = request.user

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        if Enrollment.objects.filter(student=user, course=course).exists():
            return Response({"error": "Already enrolled"}, status=400)

        if Enrollment.objects.filter(course=course, enrollment_status="ENROLLED").count() >= course.capacity:
            return Response({"error": "Course capacity is full"}, status=400)

        Enrollment.objects.create(
            student=user,
            course=course,
            enrollment_status="ENROLLED"
        )

        return Response({"message": "Enrolled successfully"}, status=201)


class DropCourseView(APIView):
    permission_classes = [IsStudent]

    def delete(self, request, course_id):
        user = request.user
        try:
            enrollment = Enrollment.objects.get(
                student=user, course_id=course_id)
        except Enrollment.DoesNotExist:
            return Response({"error": "Not enrolled"}, status=404)

        enrollment.enrollment_status = "DROPPED"
        enrollment.save()

        return Response({"message": "Dropped successfully"}, status=200)


class StudentCoursesView(generics.ListAPIView):
    serializer_class = StudentCourseListSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Course.objects.filter(enrollment__student=self.request.user, enrollment__enrollment_status="ENROLLED")


class StudentTimetableView(generics.ListAPIView):
    serializer_class = StudentTimetableSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Course.objects.filter(enrollment__student=self.request.user, enrollment__enrollment_status="ENROLLED")


#  MATERIALS

class UploadMaterialView(generics.CreateAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsProfessor]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class CourseMaterialsView(generics.ListAPIView):
    serializer_class = MaterialListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs["course_id"]
        return Material.objects.filter(course_id=course_id)


#  ANNOUNCEMENTS

class CreateAnnouncementView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsProfessor]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CourseAnnouncementsView(generics.ListAPIView):
    serializer_class = AnnouncementListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(course_id=self.kwargs["course_id"])


class AnnouncementDetailView(generics.RetrieveAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
