from django.shortcuts import render
from .models import Profile
from projects.models import Project

# Create your views here.
def profiles(request):
    devs = Profile.objects.all()
    context = {'devs':devs}
    return render(request, 'users/profiles.html', context)

def devProfile(request, pk):
    dev = Profile.objects.get(id=pk)
    projects = Project.objects.filter(owner=dev)
    context = {'dev':dev, 'projects':projects}
    return render(request, 'users/profile.html', context)