# project_management/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Project, Task, ProgressReport
from .forms import TaskSelectionForm, ProgressUpdateForm
from django.contrib.auth.models import Group
from django.contrib.auth import login
from .forms import SignupForm
from .forms import ProgressReportForm
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
    tasks = Task.objects.filter(project=project, parent_task__isnull=True)  # Get only top-level tasks


    # Group tasks by difficulty level and include sub-tasks
    tasks_by_difficulty = {}
    for task in tasks:
        level = task.difficulty
        if level not in tasks_by_difficulty:
            tasks_by_difficulty[level] = []

        # Add each task with its sub-tasks
        tasks_by_difficulty[level].append({
            'task': task,
            'sub_tasks': task.sub_tasks.all()
        })
    # Sort tasks_by_difficulty by level in descending order
    tasks_by_difficulty = dict(sorted(tasks_by_difficulty.items(), key=lambda item: item[0], reverse=True))

    context = {
        'project': project,
        'tasks': tasks,
        'tasks_by_difficulty': tasks_by_difficulty
    }
    return render(request, 'project_management/project_detail.html', context)

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
    latest_report = task.latest_progress_report()
    context = {
        'task': task,
        'latest_report': latest_report
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
def express_interest(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.candidates.add(request.user)
    task.save()
    messages.success(request, 'You have expressed interest in this task.')
    return redirect('project_detail', task.project.id)

@login_required
def withdraw_candidacy(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.candidates.remove(request.user)
    task.save()
    messages.success(request, 'You have withdrawn your candidacy for this task.')
    return redirect('project_detail', task.project.id)

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

@login_required
def add_progress_report(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = ProgressReportForm(request.POST)
        if form.is_valid():
            progress_report = form.save(commit=False)
            progress_report.task = task
            progress_report.user = request.user
            progress_report.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = ProgressReportForm()
    return render(request, 'project_management/add_progress_report.html', {'form': form, 'task': task})


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
