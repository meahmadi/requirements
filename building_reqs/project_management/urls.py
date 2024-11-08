from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('task/select/<int:task_id>/', views.select_task, name='select_task'),
    path('task/update/<int:task_id>/', views.update_progress, name='update_progress'),
]
