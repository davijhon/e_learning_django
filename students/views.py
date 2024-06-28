import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
from django.views.generic import (
    CreateView, FormView, 
    ListView, DetailView,
    TemplateView, View
)


from .forms import CourseEnrollForm
from users.forms import CustomUserCreationForm
from courses.models import (
    Course, Content, 
    ContentIsComplete, InCourse 
)




class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('students:student_course_list')


    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm


    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('students:student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    # template_name = 'students/course/list.html'
    template_name = 'account/profiles/dashboard/students/students_courses_dashboard.html'
    context_object_name = 'courses'
    

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    # template_name = 'students/course/detail.html'
    template_name = 'account/profiles/dashboard/students/students_courses_content.html'
    

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, *args, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        # get course object
        context['course'] = self.get_object()
        if 'object_id' in self.kwargs:
            # get current module
            context['content'] = Content.objects.get(id=self.kwargs['object_id'])
        else:
            pass
        return context


class StudentProfileView(TemplateView):
    template_name = 'account/profiles/dashboard/students/students_dashboard.html'




def content_is_complete(request):
    if request.is_ajax():
        data_request = json.loads(request.body)
        student = request.user

        content_complete, created = ContentIsComplete.objects.get_or_create(
            content_id=data_request['content_id'],
            student_id=student.id,
            is_complete=True,
        )
        course_progress, created = InCourse.objects.get_or_create(
            student=student,
            course=data_request['course_id'],
        )
        course_progress.add_progress(data_request['course_id'])
        course_progress.save()
        content_complete.save()

        return HttpResponse('')
