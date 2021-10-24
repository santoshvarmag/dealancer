from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.single_project, name='project'),
    path('create-project/', views.createProject, name="create-project"),
    path('update/<str:pk>/', views.editProject, name='update-project'),
    path('delete/<str:pk>/', views.deleteProject, name="delete-project"),
]
