from django.urls import path
from .views import (
    StudentRegistrationView, StudentEnrollCourseView, 
    StudentCourseListView, StudentCourseDetailView,
    StudentProfileView, content_is_complete

)

app_name = 'students'
urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<pk>/', StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<pk>/<module_id>/<object_id>/', StudentCourseDetailView.as_view(), name='student_course_detail_module'),
    path('my-profile/', StudentProfileView.as_view(), name='student_profile'),
    path('content-complete/', content_is_complete, name='content_of_module_complete'),
]