from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('logout/', views.userlogout, name='logout'),  # Ensure there's a trailing slash
    path('tasks/', views.taskList, name='tasks'),
    path('task_update/<str:pk>/', views.updateTask, name='task_update'),
    path('task_delete/<str:pk>/', views.deleteTask, name='task_delete'),
    path('profile/', views.profile_settings, name='profile_settings')
]
