from django.urls import path

from .views import (
    ManageCourseListView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    CourseModuleUpdateView,
    ModuleContentListView,
    ModuleOrderView,
    ContentOrderView,
    CourseListView,
    CourseDetailView,
    IndexView,
    InstructorProfileView,
    CoursesIntructorView,
    CourseCategoryView,
    QuizView,
    ContentDeleteView,
    AboutView,
    AllCourseListView,
    ContentCreateUpdateView,
)


app_name = "courses"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("my-profile/", InstructorProfileView.as_view(), name="profile"),
    path(
        "category/<slug:slug>/", CourseCategoryView.as_view(), name="course_categories"
    ),
    path(
        "instructor-courses/", CoursesIntructorView.as_view(), name="instructor_courses"
    ),
    path("mine/", ManageCourseListView.as_view(), name="manage_course_list"),
    path("create/", CourseCreateView.as_view(), name="course_create"),
    path("<pk>/edit/", CourseUpdateView.as_view(), name="course_edit"),
    path("<pk>/delete", CourseDeleteView.as_view(), name="course_delete"),
    path("<pk>/module/", CourseModuleUpdateView.as_view(), name="course_module_update"),
    path(
        "module/<int:module_id>/content/<model_name>/create/",
        ContentCreateUpdateView.as_view(),
        name="module_content_create",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/<id>/",
        ContentCreateUpdateView.as_view(),
        name="module_content_update",
    ),
    path(
        "content/<int:pk>/delete/",
        ContentDeleteView.as_view(),
        name="module_content_delete",
    ),
    path(
        "module/<int:module_id>/",
        ModuleContentListView.as_view(),
        name="module_content_list",
    ),
    path("module/order/", ModuleOrderView.as_view(), name="module_order"),
    path("content/order/", ContentOrderView.as_view(), name="content_order"),
    path("quiz/", QuizView.as_view(), name="quiz"),
    # path('saveans/', saveans, name='saveans'),
    # path('result/', result, name='result'),
    path("courses-list/", AllCourseListView.as_view(), name="course_list"),
    path(
        "subject/<slug:subject>/", CourseListView.as_view(), name="course_list_subject"
    ),
    path("<slug:slug>/", CourseDetailView.as_view(), name="course_detail"),
]
