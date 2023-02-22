from django.shortcuts import render


# *************** PROJECTS ****************#

def new_project(request):
    return render(request, 'projects/new_project.html')


def projects_in(request):
    return render(request, 'projects/projects_in.html')


def projects_out(request):
    return render(request, 'projects/projects_out.html')
