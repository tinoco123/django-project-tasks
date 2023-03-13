from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    if request.method == "GET":
        return render(request, 'signup.html', {
            'title': "Sign Up",
            'form': UserCreationForm
        })
    elif request.method == "POST":
        print("Hola")
        print(request.POST)
        return redirect('sign_up')
