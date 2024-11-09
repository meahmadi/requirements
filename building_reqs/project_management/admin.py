from django.contrib import admin
from .models import Project, Task, BlogPost, Map, MapLink

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('visible_to_groups',)  # This makes it easier to select multiple groups
    list_display = ('name', 'created_at')

class BlogPostAdmin(admin.ModelAdmin):
    filter_horizontal = ('visible_to_groups',)
    list_display = ('title', 'date_posted')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task)
admin.site.register(BlogPost, BlogPostAdmin)

class MapLinkInline(admin.TabularInline):
    model = MapLink
    extra = 1

class MapAdmin(admin.ModelAdmin):
    inlines = [MapLinkInline]

admin.site.register(Map, MapAdmin)

