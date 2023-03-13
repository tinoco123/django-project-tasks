from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    if request.method == "GET":
        return render(request, 'signup.html', {
            'title': "Sign Up",
            'form': UserCreationForm
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
                return HttpResponse('User created successfully')
            except:
                return render(request, 'signup.html', {
                    'title': "Sign Up",
                    'form': UserCreationForm,
                    'error': "Username already exists"
                })
        else:
            return render(request, 'signup.html', {
                'title': "Sign Up",
                'form': UserCreationForm,
                'error': 'Password does not match'
            })
