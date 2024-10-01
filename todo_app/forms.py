from django import forms
from django.forms import ModelForm
from .models import Task, Team
from django.contrib.auth.models import User

# forms.py

class TaskForm(forms.ModelForm):
    task_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add in a New Task'}))
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)

    class Meta:
        model = Task
        fields = ['task_name', 'due_date', 'task_description', 'priority', 'category', 'reminder_hours', 'team']

    def __init__(self, *args, **kwargs):
        # Get the current user from the kwargs (passed in from the view)
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        if user:
            # Filter teams to only show teams the user is part of
            self.fields['team'].queryset = Team.objects.filter(members=user)




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
        fields = ['task_name', 'task_description', 'category', 'priority', 'progress', 'completed']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Team Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe your team here...'}), required=False)

class InviteForm(forms.Form):
    username_or_email = forms.CharField(max_length=150)