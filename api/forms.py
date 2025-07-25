from django import forms

from api.models import Task
from agenda.settings import DATE_INPUT_FORMATS


class TaskForm(forms.ModelForm):
    date = forms.DateField(input_formats=DATE_INPUT_FORMATS)

    class Meta:
        model = Task
        fields = ["title", "description", "date"]
