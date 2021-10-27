from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name="profiles"),
    path('dev/<str:pk>/', views.devProfile, name='dev-profile' )
]

