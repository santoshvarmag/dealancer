from django.shortcuts import render
from .models import Profile, Skill
from projects.models import Project

# Create your views here.
def profiles(request):
    devs = Profile.objects.all()
    context = {'devs':devs}
    return render(request, 'users/profiles.html', context)

def devProfile(request, pk):
    dev = Profile.objects.get(id=pk)
    context = {'dev':dev,}
    return render(request, 'users/profile.html', context)