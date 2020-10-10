from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.views.generic import TemplateView

from kwadmin.views import HTMLTitleMixin
from kwauth.forms import KWAuthenticationForm, KWProfileForm, KWRegisterForm, KWUserExtendedProfileForm
from kwauth.models import KWUser, KWUserProfile


def login(request):
    next_url = request.GET.get('next', None)
    form = None
    if request.method == 'POST':
        form = KWAuthenticationForm(data=request.POST)
        print('form is valid:', form.is_valid())
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
        return HttpResponseRedirect(reverse('main:index'))
    return HttpResponseRedirect(request.headers["Referer"])


def register(request):
    if request.method == 'POST':
        form = KWRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.send_verify_mail()
            return HttpResponseRedirect(reverse('kwauth:user_alert', kwargs={'email': user.email}))
    else:
        form = KWRegisterForm()
    context = {
        'title': 'регистрация',
        'form': form,
    }
    return render(request, 'kwauth/register.html', context)


class UserInform(HTMLTitleMixin, TemplateView):
    page_title = f'Уведомление'
    template_name = 'kwauth/mail_alert.html'
    pk_url_kwarg = 'email'

    def get_context_data(self, email, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = KWUser.objects.get(email=email)
        return context

@login_required
def profile(request):
    if request.method == 'POST':
        form = KWProfileForm(request.POST, request.FILES, instance=request.user)
        extended_form = KWUserExtendedProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.kwuserprofile
        )
        if form.is_valid() and extended_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = KWProfileForm(instance=request.user)
        extended_form = KWUserExtendedProfileForm(
            instance=request.user.kwuserprofile
        )
    context = {
        'title': 'профиль',
        'form': form,
        'extended_form': extended_form,
    }
    return render(request, 'kwauth/profile.html', context)


def user_verify(request, email, activation_key):
    try:
        user = KWUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'error activation user: {user} ')
        return render(request, 'kwauth/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))


@receiver(post_save, sender=KWUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print('@receiver:created')
        KWUserProfile.objects.create(user=instance)
    else:
        print('@receiver:updated')
        instance.kwuserprofile.save()
