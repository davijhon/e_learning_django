from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import (
    Course,
    Module,
    Question,
    Choice,
    Video,
)

ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=["title", "description"],
    extra=2,
    can_delete=True,
)


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["title", "file", "url"]


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", "answer"]


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ["choices_text"]


ChoiceInlineFormSet = inlineformset_factory(
    Question, Choice, form=ChoiceForm, extra=4, can_delete=True
)
