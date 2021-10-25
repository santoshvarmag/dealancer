from django.shortcuts import get_object_or_404, render, redirect

from .models import Project
from .forms import ProjectForm

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    context = {'projects':projects}
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

def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('projects')

    return render(request, 'projects/project_form.html', {'form':form})

def editProject(request, pk):
    instance = get_object_or_404(Project, pk=pk)
    form = ProjectForm(instance=instance)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('projects')

    return render(request, 'projects/project_form.html', {'form':form})

def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
        
    context = {'object':project}
    return render(request, 'projects/delete.html', context)