from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')


def signup(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        passowrd_cont = request.POST.get('passwordcont')
        email = request.POST.get('email')
        
        if password == passowrd_cont:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('userlogin')
        else:
            #case the password doesnt match
            return render(request, 'signup.html', {"error": "MISMATCHED PASSWORDS"})
    return render(request, 'signup.html')

def userlogin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'userlogin.html', {'error': 'INCORRECT USERNAME OR PASSWORD'})
            
    return render(request, 'userlogin.html')

def logout(request):
    pass

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

class createList(CreateView):
    model = Task
    fields = ['task_name', 'task_description', 'completed']
    success_url = reverse_lazy('tasks')



'''
---------testing out versions--------------------------
class taskList(ListView):
    model = Task
    '''
