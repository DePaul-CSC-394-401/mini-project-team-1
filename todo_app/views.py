from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm, ProfileForm  # Ensure ProfileForm is defined in your forms.py

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
            return redirect('tasks')
        else:
            return render(request, 'userlogin.html', {'error': 'INCORRECT USERNAME OR PASSWORD'})
            
    return render(request, 'userlogin.html')

def userlogout(request):
    logout(request)
    return redirect('userlogin')  # Redirect to the login page after logout

def taskList(request):
    form = TaskForm()
    tasks = Task.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/tasks')
    context = {'tasks': tasks, 'TaskForm': form}
    return render(request, 'tasks.html', context)

def updateTask(request, pk):
    tasks = Task.objects.get(id=pk)
    form = TaskForm(instance=tasks)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=tasks)
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

# ** Added Profile Management View **
def profile_settings(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = request.user
        
        if email:
            user.email = email
            user.save()
        
        if password:
            # Handle password update
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Important to keep the user logged in
                return redirect('profile_settings')
            else:
                return render(request, 'profile.html', {'form': form, 'error': form.errors})
        
        return redirect('profile_settings')
    
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'profile.html', {'form': form})


'''
---------testing out versions--------------------------
class taskList(ListView):
    model = Task
    '''
