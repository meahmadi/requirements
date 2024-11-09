# project_management/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Project, Task
from .forms import TaskSelectionForm, ProgressUpdateForm
from django.contrib.auth.models import Group
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user with is_active=False
            messages.success(request, 'Registration successful! An admin will review your account soon.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



def user_in_project_groups(user, project):
    """
    Check if a user is in any group that has access to a project.
    """
    if user.is_superuser:
        return True  # Allow superuser to access everything
    user_groups = user.groups.all()
    return project.visible_to_groups.filter(id__in=user_groups).exists()


@login_required
def project_list(request):
    user_groups = request.user.groups.all()
    projects = Project.objects.filter(visible_to_groups__in=user_groups).distinct()
    recent_posts = BlogPost.objects.order_by('-date_posted')[:3]
    tasks_by_difficulty = {level: [] for level in range(1, 11)}
    for task in Task.objects.all():
        tasks_by_difficulty[task.difficulty].append(task)
    return render(request, 'project_management/project_list.html', {
        'projects': projects,
        'posts': recent_posts,
        'tasks_by_difficulty' : tasks_by_difficulty,
    })

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Check if the user belongs to any of the project's allowed groups
    if not user_in_project_groups(request.user, project):
        return HttpResponseForbidden("You do not have permission to view this project.")

    tasks_by_difficulty = {level: [] for level in range(1, 11)}
    for task in project.tasks.all():
        tasks_by_difficulty[task.difficulty].append(task)
    tasks = project.tasks.all()
    return render(request, 'project_management/project_detail.html', {'project': project, 'tasks': tasks, 'tasks_by_difficulty': tasks_by_difficulty})

def task_list(request):
    tasks = Task.objects.all()
    tasks_by_difficulty = {level: [] for level in range(1, 11)}
    for task in tasks:
        tasks_by_difficulty[task.difficulty].append(task)
    return render(request, 'project_management/task_list.html', {
        'tasks_by_difficulty' : tasks_by_difficulty,
        'tasks':tasks
    })

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if the user has permission to view the parent project of the task
    if not user_in_project_groups(request.user, task.project):
        return HttpResponseForbidden("You do not have permission to view this task.")
    context = {
        'task': task
    }
    return render(request, 'project_management/task_detail.html', context)

@login_required
def select_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.assigned_to = request.user
        task.is_selected = True
        task.save()
        return redirect('project_detail', project_id=task.project.id)
    return render(request, 'project_management/select_task.html', {'task': task})

@login_required
def update_progress(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=task.project.id)
    else:
        form = ProgressUpdateForm(instance=task)
    return render(request, 'project_management/update_progress.html', {'form': form, 'task': task})

from .models import BlogPost

@login_required
def blog_list(request):
    user_groups = request.user.groups.all()
    blogposts = BlogPost.objects.filter(visible_to_groups__in=user_groups).distinct().order_by('-date_posted')  # List posts from newest to oldest
    return render(request, 'project_management/blog_list.html', {'posts': blogposts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'project_management/blog_detail.html', {'post': post})


from .models import Map

def map_view(request):
    maps = Map.objects.all()  # Assuming you may have multiple maps
    return render(request, 'project_management/map_view.html', {'maps': maps})
