from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('tasks/', views.tasks, name='tasks'),
    path('login', views.sign_in, name='login'),
    path('log_out', views.log_out, name='log_out'),
    path('tasks/create', views.create_task, name='create_task')
]