from django.urls import path, include
from . import views
from django.contrib import admin
from .views import taskList, updateTask, deleteTask

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('logout', views.logout, name='logout'),
    path('tasks', views.taskList, name='tasks'),
    path('task_update/<str:pk>/', views.updateTask, name='task_update'),
    path('task_delete/<str:pk>/', views.deleteTask, name='task_delete')
]

