from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required




from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles, profilePagination

# Create your views here.
def profiles(request):
    devs, search_query = searchProfiles(request)
    custom_range, devs = profilePagination(request, devs, 3)
    

    context = {'devs':devs, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)

def devProfile(request, pk):
    dev = Profile.objects.get(id=pk)
    topSkills = dev.skill_set.exclude(description__exact='')
    otherSkills = dev.skill_set.filter(description='')
    context = {'dev':dev, 'topSkills':topSkills, 'otherskills':otherSkills}
    return render(request, 'users/profile.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.warning(request, "Username or Password incorrect")

    return render(request, 'users/login_register.html', {'page':page})


def logoutUser(request):
    logout(request)
    messages.info(request, "User was sucessfully logged out!")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created!")

            login(request, user)
            return redirect('edit-account')
        else:
            messages.warning(request, "An error has occured during the registration")            
    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    context = {'profile':profile}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
                
    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
            
    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object':skill}
    return render(request, 'delete.html', context)