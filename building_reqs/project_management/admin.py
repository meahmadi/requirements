from django.contrib import admin
from .models import Project, Task, BlogPost, Map, MapLink, ProgressReport

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('visible_to_groups',)  # This makes it easier to select multiple groups
    list_display = ('name', 'created_at')

class BlogPostAdmin(admin.ModelAdmin):
    filter_horizontal = ('visible_to_groups',)
    list_display = ('title', 'date_posted')

admin.site.register(Project, ProjectAdmin)
admin.site.register(BlogPost, BlogPostAdmin)

class MapLinkInline(admin.TabularInline):
    model = MapLink
    extra = 1

class MapAdmin(admin.ModelAdmin):
    inlines = [MapLinkInline]

admin.site.register(Map, MapAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to')
    fields = ('title', 'description', 'status', 'assigned_to', 'candidates' )  # Include candidates for selection
    filter_horizontal = ('candidates',)  # Optional: Adds a widget to manage many-to-many fields

admin.site.register(Task, TaskAdmin)

admin.site.register(ProgressReport)
