from django.contrib import admin
from .models import Project, Task, BlogPost

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(BlogPost)

