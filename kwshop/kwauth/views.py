from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

# Create your views here.
from kwauth.forms import KWAuthenticationForm


def login(request):
    form = KWAuthenticationForm()
    context = {
        'title': 'аутентификация',
        'form': form
    }
    return render(request, 'kwauth/login.html', context)

def logout(request):
    pass


def register(request):
    pass

def profile(request):
    pass
