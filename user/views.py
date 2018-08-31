from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import auth
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(reverse('index'))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'user/login.html',context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('user:login'))