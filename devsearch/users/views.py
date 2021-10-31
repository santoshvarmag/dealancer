from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile

# Create your views here.
def profiles(request):
    devs = Profile.objects.all()
    context = {'devs':devs}
    return render(request, 'users/profiles.html', context)

def devProfile(request, pk):
    dev = Profile.objects.get(id=pk)
    context = {'dev':dev,}
    return render(request, 'users/profile.html', context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.warning(request, "Username or Password incorrect")

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.success(request, "User was sucessfully logged out!")
    return redirect('login')