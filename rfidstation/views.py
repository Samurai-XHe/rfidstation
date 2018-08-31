from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect(reverse('user:login'))