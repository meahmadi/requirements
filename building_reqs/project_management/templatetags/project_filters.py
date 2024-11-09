# project_filters.py
from django import template
from ..views import user_in_project_groups

register = template.Library()

@register.filter
def can_view_project(user, project):
    return user_in_project_groups(user, project)
