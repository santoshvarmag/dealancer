from os import name
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.profiles, name="profiles"),
    path('dev/<str:pk>/', views.devProfile, name='dev-profile' ),
    path('account/', views.userAccount, name="account"),
    path('edit_account/', views.editAccount, name='edit-account'),
    path('create_skill/', views.createSkill, name='create-skill'),
    path('update_skill/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete/<str:pk>/', views.deleteSkill, name='delete-skill'),
]

