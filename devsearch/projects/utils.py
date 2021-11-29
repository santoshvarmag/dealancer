from django.db.models import Q

from projects.models import Project, Tag

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # tags = Tag.objects.filter(name__icontains=search_query)
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        # Another way to filter the child model as below
        Q(tags__name__icontains=search_query) |
        Q(owner__name__icontains=search_query) 
    )

    return projects, search_query