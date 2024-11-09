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

from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False  # User needs to be approved by admin
        if commit:
            user.save()
        return user
