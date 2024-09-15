from django.urls import path, include
from . import views
from django.contrib import admin
from .views import taskList, createList

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('logout', views.logout, name='logout'),
    path('tasks', views.taskList, name='tasks')
]

