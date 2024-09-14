from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Task


def index(request):
    return render(request, 'index.html')


def signup(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password= request.POST.get('password')
        passowrdcont= request.POST.get('passwordcont')
        email= request.POST.get('email')
        
        myuser = User.objects.create(username, password, email)
        myuser.save()
        return redirect('signin')
    return render(request, 'signup.html')

def userlogin(request):
    return render(request, 'userlogin.html')

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return render(request, 'signin.html')
        else:
            return redirect('index')
            
    return render(request, 'userlogin.html')

def logout(request):
    pass

def taskList(request):
    tasks = Task.objects.all()
    context = {'tasks':tasks}
    return render(request, 'task_list.html', context)

'''
---------testing out versions--------------------------
class taskList(ListView):
    model = Task
    '''
