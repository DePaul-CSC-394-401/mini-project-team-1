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
    path('profile/', views.profile_settings, name='profile_settings'),  # Added profile management
    path('task_archive/<str:pk>/', views.archiveTask, name='task_archive'),
    path('archived_tasks/', views.archivedTasks, name='archived_tasks'),
    path('task_restore/<str:pk>/', views.restoreTask, name='task_restore'),
    path('task_add', views.AddTask, name='task_add'),
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/', views.view_teams, name='view_teams'),
    path('team/<int:team_id>/', views.view_team, name='view_team'),
    path('team/<int:team_id>/invite/', views.invite_member, name='invite_member'),
]
