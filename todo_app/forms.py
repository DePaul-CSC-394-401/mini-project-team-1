from django import forms
from django.forms import ModelForm
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    task_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add in a New Task'}))
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'priority']

# ** Email Update Form for Profile Management **
class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']  # Only include the email field
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Update your email'}),
        }

# Form for updating tasks (includes the 'completed' field)
class TaskUpdateForm(forms.ModelForm):
    task_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Update Task Name'}))

    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'priority', 'completed']
