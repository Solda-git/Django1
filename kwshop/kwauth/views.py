from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from kwauth.forms import KWAuthenticationForm, KWProfileForm, KWRegisterForm


def login(request):

    next_url = request.GET.get('next', None)
    form = None
    if request.method == 'POST':
        form = KWAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                next_url = request.POST.get('next_url', None)
                auth.login(request, user)
                if next_url:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("main:index"))
    elif request.method == 'GET':
        form = KWAuthenticationForm()
        context = {
            'title': 'аутентификация',
            'form': form,
            'next': next_url,
        }
        return render(request, 'kwauth/login.html', context)


def logout(request):
    auth.logout(request)
    if 'cart' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect (reverse('main:index'))
    return HttpResponseRedirect(request.headers["Referer"])

def register(request):
    if request.method == 'POST':
        form = KWRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = KWRegisterForm()
    context = {
        'title': 'регистрация',
        'form': form,
    }
    return render(request, 'kwauth/register.html', context)


def profile(request):
    if request.method == 'POST':
        form = KWProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = KWProfileForm(instance=request.user)
    context = {
        'title': 'профиль',
        'form': form
    }
    return render(request, 'kwauth/profile.html', context)
