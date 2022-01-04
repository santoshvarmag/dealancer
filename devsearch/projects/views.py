from django.core import paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, projectsPagination

# Create your views here.


def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = projectsPagination(request, projects, 3)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range, 'paginator': paginator}
    return render(request, 'projects/projects.html', context)


def single_project(request, pk):
    project = Project.objects.get(pk=pk)
    form = ReviewForm()

    project_reviews = project.review_set.all()
    project_tags = project.tags.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        # Update project vote count
        project.getVoteCount

        messages.success(request, "Your review was successfully submitted!")
        return redirect('project', pk=project.id)

    context = {
        'project': project,
        'project_reviews': project_reviews,
        'project_tags': project_tags,
        'form': form
    }

    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        tags = request.POST.get('newTags').replace(',', " ").split()

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    return render(request, 'projects/project_form.html', {'form': form})


@login_required(login_url='login')
def editProject(request, pk):
    profile = request.user.profile
    instance = profile.project_set.get(id=pk)
    form = ProjectForm(instance=instance)
    if request.method == "POST":
        newTags = request.POST.get('newTags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            project = form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    return render(request, 'projects/project_form.html', {'form': form})


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'delete.html', context)
