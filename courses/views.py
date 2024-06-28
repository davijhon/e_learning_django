from django.contrib import messages
from django.db.models import Count
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    View,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from users.models import UserProfile
from students.forms import CourseEnrollForm

# ItemBase,
from .models import (
    Course,
    Module,
    Content,
    Subject,
    Question,
    Choice,
    Video,
)
from blog.models import Post
from .forms import (
    # ChoiceFormSet
    ModuleFormSet,
    QuestionForm,
    VideoForm,
    ChoiceInlineFormSet,
)


# Take one or multiple answer in the quiz, and evaluated if are correct
def validating_if_correct(module_quiz, user_answer):
    quiz = Question.objects.get(module=module_quiz)

    if user_answer == quiz.answer:
        return True
    return False


class IndexView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        subjects = Subject.objects.all()
        featured_courses = Course.objects.filter(
            featured=True,
        )[:7]
        featured_posts = Post.objects.filter(
            is_publicated=True,
        )[:2]

        try:
            user_profile = UserProfile.objects.get_or_create(user=self.request.user)
        except:
            user_profile = None

        context = super().get_context_data(**kwargs)
        context["profile"] = user_profile
        context["featured_courses"] = featured_courses
        context["featured_posts"] = featured_posts
        context["subjects"] = subjects
        return context


class CourseCategoryView(ListView):

    def get(self, request, slug, *args, **kwargs):
        courses = Course.objects.filter(subject__slug=slug)
        subject = Subject.objects.get(slug=slug)
        context = {"courses": courses, "subject": subject}
        return render(request, "pages/course_category.html", context)


class AboutView(TemplateView):
    template_name = "pages/about.html"


class CoursesIntructorView(PermissionRequiredMixin, TemplateView):
    template_name = (
        "account/profiles/dashboard/instructor/instructor_courses_dashboard.html"
    )
    permission_required = "courses.change_course"


class InstructorProfileView(PermissionRequiredMixin, TemplateView):
    template_name = "account/profiles/dashboard/instructor/instructor_dashboard.html"
    permission_required = "courses.change_course"


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("courses:manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("courses:manage_course_list")
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(PermissionRequiredMixin, OwnerCourseMixin, ListView):
    # template_name = 'courses/manage/course/list.html'
    template_name = (
        "account/profiles/dashboard/instructor/instructor_courses_dashboard.html"
    )
    permission_required = "courses.change_course"


class AllCourseListView(ListView):
    model = Course
    template_name = "pages/course_list.html"
    context_object_name = "courses"
    paginate_by = 5


class CourseListView(TemplateResponseMixin, View):
    model = Course
    # template_name = 'account/profiles/dashboard/instructor/instructor_courses_dashboard.html'
    template_name = "courses/course/list.html"

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count("courses"))
        courses = Course.objects.annotate(total_modules=Count("modules"))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {"subjects": subjects, "subject": subject, "courses": courses}
        )


class CourseDetailView(DetailView):
    model = Course
    # template_name = 'courses/course/detail.html'
    template_name = "courses/course/course_description.html"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(initial={"course": self.object})
        return context


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = "courses.add_course"


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = "courses.change_course"


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
    success_url = reverse_lazy("courses:manage_course_list")
    permission_required = "courses.delete_course"


class CourseModuleUpdateView(PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name = "courses/manage/module/formset.html"
    course = None
    permission_required = "courses.change_course"

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({"course": self.course, "formset": formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("courses:manage_course_list")
        return self.render_to_response({"course": self.course, "formset": formset})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)

        module = content.module
        content.item.delete()
        content.delete()
        return redirect("module_content_list", module.id)


class ModuleContentListView(PermissionRequiredMixin, TemplateResponseMixin, View):
    template_name = "courses/manage/module/content_list.html"
    permission_required = "courses.change_course"

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        content = Content.objects.filter(module=module)
        ctx = {
            "content": content,
            "module": module,
        }
        return self.render_to_response(ctx)


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = None

    def get_model(self, model_name):
        if model_name in ["video", "question"]:
            return apps.get_model(app_label="courses", model_name=model_name)

        return None

    def get_form(self, model, model_name, *args, **kwargs):
        if model_name == "video":
            self.template_name = "courses/video/create_video.html"
            Form = VideoForm(instance=self.obj)
            return Form, None
        else:
            self.template_name = "courses/quiz/form.html"
            Form = QuestionForm(instance=self.obj)
            Formset = ChoiceInlineFormSet(instance=self.obj)

            return Form, Formset

    def dispatch(self, request, module_id, model_name, id=None):
        course = Course.objects.get(modules=module_id)
        if course.owner != request.user:
            raise PermissionDenied

        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id)

        return super(ContentCreateUpdateView, self).dispatch(
            request, module_id, model_name, id
        )

    def get(self, request, module_id, model_name, id=None):
        form, formset = self.get_form(
            self.model,
            model_name,
        )
        return self.render_to_response(
            {"form": form, "formset": formset, "object": self.obj}
        )

    def post(self, request, module_id, model_name, id=None):
        module = Module.objects.get(id=self.module.id)

        if model_name == "video":
            if not id:
                form = VideoForm(self.request.POST, self.request.FILES)
                # form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

                if form.is_valid():
                    video_title = form.cleaned_data.get("title")
                    video_file = form.cleaned_data.get("file")
                    video_url = form.cleaned_data.get("url")

                    video = Video.objects.create(
                        title=video_title, file=video_file, url=video_url
                    )

                    module.has_video = True
                    module.save()
                    video.save()
                    Content.objects.create(module=self.module, item=video)

                    messages.info(request, "Video Saved")
                    return redirect("courses:module_content_list", self.module.id)

                messages.info(request, "Error, Something happend at save the video")
                return redirect("courses:module_content_list", self.module.id)
            else:
                form = VideoForm(
                    self.request.POST, self.request.FILES, instance=self.obj.id
                )

                if form.is_valid():
                    video = form.save(commit=False)
                    video.save()

                    messages.info(request, "Video Saved")
                    return redirect("courses:module_content_list", self.module.id)

                messages.info(request, "Error, Something happend at save the video")
                return redirect("courses:module_content_list", self.module.id)

        else:  # if model_name is 'question'
            if not id:
                form = QuestionForm(self.request.POST)
                formset = ChoiceInlineFormSet(self.request.POST)

                if form.is_valid():
                    question = form.save(commit=False)

                    module.has_quiz = True
                    module.save()
                    question.save()
                    Content.objects.create(module=module, item=question)

                    if formset.is_valid():
                        formset.instance = question
                        formset.save()

                    messages.info(request, "Quiz Saved")
                    return redirect("courses:module_content_list", self.module.id)

                messages.info(request, "Error, Something happend at save the video")
                return redirect("courses:module_content_list", self.module.id)
            else:
                form = QuestionForm(self.request.POST, instance=self.obj)
                formset = ChoiceInlineFormSet(self.request.POST, instance=self.obj)

                if form.is_valid():
                    question = form.save(commit=False)
                    Content.objects.get_or_create(module=module)

                    module.has_quiz = True
                    module.save()
                    question.save()

                    if formset.is_valid():
                        formset.instance = question
                        formset.save()

                    messages.info(request, "Quiz Saved")
                    return redirect("courses:module_content_list", self.module.id)

                messages.info(request, "Error, Something happend at save the video")
                return redirect("courses:module_content_list", self.module.id)


class QuizView(ListView):
    model = Question
    template_name = "courses/quiz/quiz.html"
    context_object_name = "questions"


# def result(request, module_id):
#     question = Question.objects.get_object_or_404(module=module_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         messages.error(self.request, "You didn't select a choice.")
#         return redirect("course:quiz")
#     # else:
#     #     answer = question.answer
#     #     if selecte_choice == answer:


# def result(request):
#     ans = request.GET['ans']
#     is_correct = validating_if_correct(module_id, ans)
#     if is_correct:
#         return render(request, 'courses/quiz/result.html')

#     messages.error(self.request, "That is not the answer, try again!")
#     return redirect("course:quiz")

# def saveans(request):
#     ans = request.GET['ans']


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({"saved": "OK"})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__ower=request.user).update(
                order=order
            )
        return self.render_json_response({"saved": "OK"})
