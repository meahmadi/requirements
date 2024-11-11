
from django.db import models
from django.contrib.auth.models import Group, User
from django.urls import reverse
from ckeditor.fields import RichTextField
import jdatetime

def convert_to_persian_numbers(date_str):
    persian_numbers = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', 
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
    }
    return ''.join(persian_numbers.get(char, char) for char in date_str)


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    visible_to_groups = models.ManyToManyField(Group, blank=True, related_name="visible_projects")
    github_repo_url = models.URLField(blank=True, null=True)  # URL of the GitHub repository
    github_wiki_url = models.URLField(blank=True, null=True)  # URL of the GitHub wiki page

    def get_jalali_date(self):
        # Convert the datetime field to Jalali date
        return convert_to_persian_numbers(jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d'))

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="sub_tasks")
    title = models.CharField(max_length=200)
    description = RichTextField()
    github_issue_url = models.URLField(blank=True, null=True)  # URL of the GitHub issue


    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_tasks')
    candidates = models.ManyToManyField(User, related_name='task_candidates', blank=True)

    status = models.CharField(max_length=20, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    progress_report = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_selected = models.BooleanField(default=False)
    difficulty = models.PositiveIntegerField(default=1)

    def get_create_jalali_date(self):
        return convert_to_persian_numbers(jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d'))
    def get_update_jalali_date(self):
        return convert_to_persian_numbers(jdatetime.datetime.fromgregorian(datetime=self.updated_at).strftime('%Y/%m/%d'))
    def latest_progress_report(self):
        # Fetch the latest report
        return self.progress_reports.order_by('-created_at').first()
    def __str__(self):
        return f"{self.title} ({self.status})"

class ProgressReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="progress_reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_jalali_date(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created_at).strftime('%Y/%m/%d')

    def __str__(self):
        return f"گزارش کار {self.task.title} توسط {self.user.username}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    visible_to_groups = models.ManyToManyField(Group, blank=True, related_name="visible_blogposts")

    def get_post_jalali_date(self):
        return convert_to_persian_numbers(jdatetime.datetime.fromgregorian(datetime=self.date_posted).strftime('%Y/%m/%d'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])


class Map(models.Model):
    title = models.CharField(max_length=100)
    svg_file = models.FileField(upload_to='maps/')
    description = RichTextField(blank=True)

    def __str__(self):
        return self.title

class MapLink(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name="links")
    element_id = models.CharField(max_length=100, help_text="ID of the SVG element to make clickable")
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    blog_post = models.ForeignKey('BlogPost', on_delete=models.SET_NULL, null=True, blank=True)

    def get_url(self):
        # Return the appropriate URL based on the linked model
        if self.project:
            return reverse('project_detail', args=[self.project.id])
        elif self.task:
            return reverse('task_detail', args=[self.task.id])
        elif self.blog_post:
            return reverse('blog_detail', args=[self.blog_post.id])
        return '#'

    def __str__(self):
        return f"Link on {self.map.title} to {self.project or self.task or self.blog_post}"
