from django.urls import path
from .views import *

urlpatterns = [

    # DEPARTMENTS
    # Tested
    path("department/showall/", ShowAllDepartmentsView.as_view(),
         name="departments_list"),
    # Tested
    path("department/create/", RegisterDepartmentView.as_view(),
         name="department_create"),
    # ---------------------------------------------------------------------
    # COURSES
    # Tested
    path("courses/", ShowAllCoursesView.as_view(), name="courses_list"),
    # Tested
    path("courses/create/", RegisterCourseView.as_view(), name="course_create"),
    # Tested
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    # Tested
    path("courses/<int:pk>/update/",
         UpdateCourseView.as_view(), name="course_update"),
    # Tested
    path("courses/<int:pk>/delete/",
         DeleteCourseView.as_view(), name="course_delete"),
    # ---------------------------------------------------------------------
    # PROFESSOR
    # Tested
    path("professor/courses/", ProfessorCoursesView.as_view(),
         name="professor_courses"),
    # Tested
    path("professor/courses/<int:course_id>/students/", ProfessorCourseStudentsView.as_view(),
         name="professor_course_students"),
    # ---------------------------------------------------------------------
    # ENROLLMENT
    # Tested
    path("enroll/<int:course_id>/",
         EnrollInCourseView.as_view(), name="course_enroll"),
    # Tested
    path("drop/<int:course_id>/", DropCourseView.as_view(), name="course_drop"),
    # Tested
    path("student/courses/", StudentCoursesView.as_view(), name="student_courses"),
    # Tested
    path("student/timetable/", StudentTimetableView.as_view(),
         name="student_timetable"),
    # ---------------------------------------------------------------------
    # MATERIALS
    # Tested
    path("materials/upload/", UploadMaterialView.as_view(), name="material_upload"),
    # Tested
    path("materials/<int:course_id>/",
         CourseMaterialsView.as_view(), name="course_materials"),
    # ---------------------------------------------------------------------
    # ANNOUNCEMENTS
    # Tested
    path("announcements/create/", CreateAnnouncementView.as_view(),
         name="announcement_create"),
    # Tested
    path("course announcements/<int:course_id>/",
         CourseAnnouncementsView.as_view(), name="course_announcements"),

    path("announcement/<int:pk>/", AnnouncementDetailView.as_view(),
         name="announcement_detail"),
]
