# project_management/forms.py
from django import forms
from .models import Task

class TaskSelectionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []  # No fields, as we only need to trigger the selection action

class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['progress_report']
        widgets = {
            'progress_report': forms.Textarea(attrs={'rows': 4}),
        }
