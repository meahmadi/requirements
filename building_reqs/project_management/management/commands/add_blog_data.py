from django.core.management.base import BaseCommand
from project_management.models import Project, Task, BlogPost

from random import choice, randint

class Command(BaseCommand):
    help = "Adds sample blog data with related projects and tasks to the database."

    def handle(self, *args, **kwargs):
        # Delete any existing blogs to avoid duplicates
        BlogPost.objects.all().delete()

        # Sample Persian blog titles and contents
        blog_titles = [
            "پیشرفت‌های اخیر پروژه",
            "نکاتی درباره وظایف پیچیده",
            "نحوه بهبود عملکرد پروژه",
            "چالش‌های پیش رو در پروژه",
            "گزارش وضعیت وظایف",
        ]
        
        blog_contents = [
            "این یک پست وبلاگ است که درباره پیشرفت‌های اخیر در پروژه صحبت می‌کند.",
            "در این پست به نکات مهم درباره وظایف پیچیده و نحوه انجام آنها اشاره شده است.",
            "هدف این پست بهبود عملکرد پروژه و ارائه راهکارهای موثر است.",
            "در این مقاله، چالش‌های پیش رو در پروژه مورد بحث قرار می‌گیرد.",
            "این یک گزارش وضعیت از وظایف جاری پروژه است و شامل پیشرفت‌ها و موانع می‌باشد.",
        ]

        # Retrieve all projects and tasks
        projects = list(Project.objects.all())
        tasks = list(Task.objects.all())

        # Add 10 sample blog entries with random projects and tasks
        for i in range(10):
            project = choice(projects)
            # Pick a task related to the project if available
            related_tasks = Task.objects.filter(project=project)
            task = choice(related_tasks) if related_tasks else None

            BlogPost.objects.create(
                title=blog_titles[i % len(blog_titles)],
                content=blog_contents[i % len(blog_contents)],
                project=project,
                task=task,
            )

        self.stdout.write(self.style.SUCCESS("Sample blog data added successfully!"))
