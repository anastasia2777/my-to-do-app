from django.urls import path
from . import views
from .views import TaskUpdateView

app_name='todo'

urlpatterns=[
    path('', views.task_list, name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
]