from django.db import models
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField

User = get_user_model()


class Subject(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to="images/")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_categories", kwargs={"slug": self.slug})


class Course(models.Model):
    owner = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    image = models.ImageField(
        "Imagen Referencial", upload_to="imagenes/", max_length=255
    )
    students = models.ManyToManyField(User, related_name="courses_joined", blank=True)
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("payment:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("payment:remove-from-cart", kwargs={"slug": self.slug})


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])
    has_video = models.BooleanField(default=False)
    has_quiz = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return "{}. {}".format(self.order, self.title)


class Video(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to="files")
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

    # def render(self):
    #     return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})
    def render(self):
        return render_to_string("courses/content/video.html", {"item": self})


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

    # def render(self):
    #     return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})
    def render(self):
        return render_to_string("courses/quiz/quiz.html", {"item": self})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choices_text


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    # video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True)
    # quiz = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("video", "question")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "content of {}".format(self.module.title)


class ContentIsComplete(models.Model):
    """This is a Class to list which content is completed for
    a student"""

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)


class InCourse(models.Model):
    """
    This is a object that store the progress of a student in a course
    """

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} have a {}% of {} course completed".format(
            self.student.email,
            self.progress,
            self.course.title,
        )

    def add_progress(self, course_id):
        total_content = Content.objects.filter(module__course=course_id).count()
        content_porcent = (1 / total_content) * 100
        self.progress += content_porcent
