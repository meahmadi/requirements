# project_management/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import TaskSelectionForm, ProgressUpdateForm

def project_list(request):
    projects = Project.objects.all()
    recent_posts = BlogPost.objects.order_by('-date_posted')[:3]
    tasks_by_difficulty = {level: [] for level in range(1, 11)}
    for task in Task.objects.all():
        tasks_by_difficulty[task.difficulty].append(task)
    return render(request, 'project_management/project_list.html', {
        'projects': projects,
        'posts': recent_posts,
        'tasks_by_difficulty' : tasks_by_difficulty,
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
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

def blog_list(request):
    posts = BlogPost.objects.order_by('-date_posted')  # List posts from newest to oldest
    return render(request, 'project_management/blog_list.html', {'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'project_management/blog_detail.html', {'post': post})
