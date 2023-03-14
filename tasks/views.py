from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm


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


def tasks(request):
    return render(request, 'tasks.html', {
        'title': 'Tasks'
    })


def log_out(request):
    logout(request)
    return redirect('index')


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html', {
            'title': 'Sign In',
            'form': AuthenticationForm
        })
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
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
        

def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'title': 'Create task',
            'form': CreateTaskForm
        })
    elif request.method == 'POST':
        print(request.POST)
        return render(request, 'create_task.html', {
            'title': 'Create task',
            'form': CreateTaskForm
        })