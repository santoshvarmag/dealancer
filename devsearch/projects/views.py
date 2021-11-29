from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import Project
from .forms import ProjectForm
from .utils import searchProjects

# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    context = {'projects':projects, 'search_query': search_query}
    return render(request, 'projects/projects.html', context)


def single_project(request, pk):
    project = Project.objects.get(pk=pk)
    project_reviews = project.review_set.all()
    project_tags = project.tags.all()
    context = {
        'project':project, 
        'project_reviews': project_reviews,
        'project_tags':project_tags
        }
    print(project)
    return render(request, 'projects/single-project.html', context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save() 
            return redirect ('account')

    return render(request, 'projects/project_form.html', {'form':form})

@login_required(login_url='login')
def editProject(request, pk):
    profile = request.user.profile
    instance = profile.project_set.get(id=pk)
    form = ProjectForm(instance=instance)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('account')

    return render(request, 'projects/project_form.html', {'form':form})

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
        
    context = {'object':project}
    return render(request, 'delete.html', context)