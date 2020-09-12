from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from kwadmin.forms import KWAdminUserCreateForm


@user_passes_test (lambda u: u.is_superuser)
def index(request):
    object_list = get_user_model().objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': 'пользователи',
        'object_list': object_list,
    }
    return render(request, 'kwadmin/index.html', context)


@user_passes_test (lambda u: u.is_superuser)
def user_create(request):
    user_form = None
    if request.method == 'POST':
        user_form = KWAdminUserCreateForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('kwadmin:index'))
        else:
            user_form = KWAdminUserCreateForm()
    context = {
        'title': 'новый пользователь',
        'user_form': user_form,
    }
    return render(request, 'kwadmin/user_update.html', context=context)