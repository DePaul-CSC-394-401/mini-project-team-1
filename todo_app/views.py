from datetime import timedelta, timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm, TaskUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import models
from django.utils import timezone




def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')  # Fixed typo from `passworda` to `password`
        password_cont = request.POST.get('passwordcont')
        email = request.POST.get('email')

        if password == password_cont:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('userlogin')
        else:
            return render(request, 'signup.html', {"error": "MISMATCHED PASSWORDS"})
    return render(request, 'signup.html')

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            tasks = Task.objects.filter(user=user)
            reminder_tasks = [task for task in tasks if task.due_date and task.due_date - timedelta(hours=task.reminder_hours) <= timezone.now()]
            if reminder_tasks:
                request.session['reminder'] = f"You have {len(reminder_tasks)} task(s) due soon!"
            return redirect('tasks')
        else:
            return render(request, 'userlogin.html', {'error': 'INCORRECT USERNAME OR PASSWORD'})
            
    return render(request, 'userlogin.html')

def userlogout(request):
    logout(request)
    return redirect('userlogin')  # Redirect to the login page after logout


def taskList(request):
    form = TaskForm()  # Form for creating a new task
    query = request.GET.get('q')  # Capture the search query
    query2 = request.GET.get('c') # Capture the category search query

    tasks = Task.objects.filter(user=request.user, archived=False)  # Filter to show only non-archived tasks

    # This code will filter tasks by the search query (if provided)
    if query:
        tasks = Task.objects.filter(task_name__icontains=query) | Task.objects.filter(task_description__icontains=query)

    # This code will filter the tasks by the category query
    if query2:
        tasks = Task.objects.filter(category__icontains=query2)

    if request.method == 'POST':
        # Process task creation via POST request
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Don't save to the database yet
            if not task.due_date:
                task.due_date = None
            task.user = request.user  # Automatically associate the task with the logged-in user
            task.save()  # Save the task to the database
        return redirect('/tasks')

    # Sort tasks by priority from high to low
    tasks = tasks.order_by(
        models.Case(
            models.When(priority='High', then=0),
            models.When(priority='Medium', then=1),
            models.When(priority='Low', then=2),
            default=3,
            output_field=models.IntegerField()
        )
    )

    # If no tasks are found based on the query, throw this error
    if not tasks.exists() and query:
        error_message = "No such item found."
    else:
        error_message = ""

    #checks for reminder message
    reminder_message = request.session.pop('reminder', None)

    context = {'tasks': tasks, 'TaskForm': form, 'error_message': error_message, 'reminder_message': reminder_message}

    if not tasks.exists() and query2:
        error_message = "No such item found."
    else:
        error_message = ""

    context = {'tasks': tasks, 'TaskForm': form, 'error_message': error_message}
    return render(request, 'tasks.html', context)


def updateTask(request, pk):
    tasks = Task.objects.get(id=pk)
    form = TaskUpdateForm(instance=tasks) 
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=tasks)
        if form.is_valid():
            form.save()
        return redirect('/tasks')
    context = {'TaskForm': form}
    return render(request, 'task_update.html', context)

def deleteTask(request, pk):
    tasks = Task.objects.get(id=pk)
    if request.method == 'POST':
        tasks.delete()
        return redirect('/tasks')
    context = {'tasks': tasks}
    return render(request, 'task_delete.html', context)

# ** Updated Profile Management View to handle email and password separately ** 
def profile_settings(request):
   # Handle email form submission
   if request.method == 'POST' and 'update_email' in request.POST:
       email = request.POST.get('email')
       if email:
           request.user.email = email
           request.user.save()
           return redirect('tasks')

   # Handle password form submission
   if request.method == 'POST' and 'change_password' in request.POST:
       password_form = PasswordChangeForm(user=request.user, data=request.POST)
       if password_form.is_valid():
           user = password_form.save()
           update_session_auth_hash(request, user)  # Keep the user logged in after password change
           return redirect('tasks')
       else:
           return render(request, 'profile.html', {'password_form': password_form, 'error': 'Invalid password change'})

   # Load the forms if GET request
   else:
       password_form = PasswordChangeForm(user=request.user)
   return render(request, 'profile.html', {'password_form': password_form})


def archiveTask(request, pk):
    task = Task.objects.get(id=pk)
    
    if request.method == 'POST':  
        task.archived = True  
        task.save()  
        return redirect('tasks')  
    return redirect('tasks')  

# View to list archived tasks
def archivedTasks(request):
    tasks = Task.objects.filter(user=request.user, archived=True)  # Show only archived tasks
    context = {'tasks': tasks}
    return render(request, 'archived_tasks.html', context)

def restoreTask(request, pk):
    task = Task.objects.get(id=pk)
    task.archived = False  # Restore the task by setting archived to False
    task.save()
    return redirect('archived_tasks')




'''
---------testing out versions--------------------------
class taskList(ListView):
    model = Task
    '''
