from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html', {
        'title': 'Home'
    })


def sign_up(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'title': "Sign Up",
            'form': UserCreationForm,
        })
    elif request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            # Register user
            try:
                username = request.POST['username']
                password = request.POST['password1']
                new_user = User.objects.create_user(
                    username=username, password=password)
                new_user.save()
                login(request, new_user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'title': "Sign Up",
                    'form': UserCreationForm,
                    'error': "Username already exists",
                })
        else:
            return render(request, 'signup.html', {
                'title': "Sign Up",
                'form': UserCreationForm,
                'error': 'Password does not match',
            })


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html', {
            'title': 'Sign In',
            'form': AuthenticationForm
        })
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'sign_in.html', {
                'title': 'Sign In',
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')


@login_required
def log_out(request):
    logout(request)
    return redirect('index')


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html', {
        'title': 'Tasks',
        'tasks': tasks,
        'type_of_tasks': 'Tasks Pending'
    })


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, date_completed__isnull=False).order_by('date_completed')
    return render(request, 'tasks.html', {
        'title': 'Tasks',
        'tasks': tasks,
        'type_of_tasks': 'Tasks Completed'
    })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'title': 'Create task',
            'form': CreateTaskForm
        })
    elif request.method == 'POST':
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'title': 'Create task',
                'form': CreateTaskForm,
                'error': 'Please provide valid data'
            })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = CreateTaskForm(instance=task)
        return render(request, "task_detail.html", {
            'title': 'Task detail',
            'task': task,
            'form': form
        })
    elif request.method == 'POST':
        try:
            form = CreateTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, "task_detail.html", {
                'title': 'Task detail',
                'task': task,
                'form': form,
                'error': 'There was an error trying to update'
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
