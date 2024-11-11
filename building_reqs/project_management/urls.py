from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('task/select/<int:task_id>/', views.select_task, name='select_task'),
    path('task/update/<int:task_id>/', views.update_progress, name='update_progress'),
    path('tasks/', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'), 
    path('task/<int:task_id>/express_interest/', views.express_interest, name='express_interest'),
    path('task/<int:task_id>/withdraw_candidacy/', views.withdraw_candidacy, name='withdraw_candidacy'),
    path('task/add_progress_report/<int:task_id>/', views.add_progress_report, name='add_progress_report'),
    path('maps/', views.map_view, name='map_view'),
    path('signup/', views.signup_view, name='signup'),
]

