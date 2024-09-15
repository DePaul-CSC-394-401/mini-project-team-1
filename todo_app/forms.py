from django import forms
from django.forms import ModelForm
from .models import Task

class TaskForm(forms.ModelForm):
    task_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add in a New Task'}))

    class Meta:
        model = Task
        fields = "__all__"