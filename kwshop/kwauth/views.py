from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from kwauth.forms import KWAuthenticationForm, KWProfileForm, KWRegisterForm


def login(request):
    form = None
    if request.method == 'POST':
        form = KWAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('main:index'))
    elif request.method == 'GET':
        form = KWAuthenticationForm()
        context = {
            'title': 'аутентификация',
            'form': form
        }
        return render(request, 'kwauth/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def register(request):
    form = KWRegisterForm
    context = {
        'title': 'регистрация',
        'form': form
    }
    return render(request, 'kwauth/login.html', context)

def profile(request):
    form = KWProfileForm
    context = {
        'title': 'профиль',
        'form': form
    }
    return render(request, 'kwauth/login.html', context)
