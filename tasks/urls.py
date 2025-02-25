from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home/', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/completed', views.completed_tasks, name='completed_tasks'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.signin, name='login'),
    path('tasks/create', views.create_task, name='create_task'),
    path('tasks/<int:id>', views.task_detail, name='task_detail'),
    path('tasks/<int:id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:id>/delete', views.delete_task, name='delete_task'),
]