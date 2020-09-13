from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from kwadmin.forms import KWAdminUserCreateForm, KWAdminUserUpdateForm
from main.models import ProductCat

#
# @user_passes_test (lambda u: u.is_superuser)
# def index(request):
#     object_list = get_user_model().objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     context = {
#         'title': 'пользователи',
#         'object_list': object_list,
#     }
#     return render(request, 'kwadmin/templates/kwauth/kwuser_list.html', context)


class SuperUserCheckMixin:
    @method_decorator (user_passes_test (lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super ().dispatch (request, *args, **kwargs)

class HTMLTitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['title'] = self.page_title
        return data

class UserList(SuperUserCheckMixin, HTMLTitleMixin, ListView):
    page_title = 'пользователи'
    model = get_user_model()



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


@user_passes_test (lambda u: u.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == 'POST':
        user_form = KWAdminUserUpdateForm (request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('kwadmin:index'))
    else:
        user_form = KWAdminUserUpdateForm (instance=user)
    context = {
        'title': 'редактирование',
        'user_form': user_form,
    }
    return render(request, 'kwadmin/user_update.html', context=context)



@user_passes_test (lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect (reverse ('kwadmin:index'))
    context = {
        'title': 'удаление пользоателя',
        'user': user,
    }
    return render(request, 'kwadmin/user_delete.html', context)


# @user_passes_test (lambda u: u.is_superuser)
# def get_categories (request):
#
#     context = {
#         'title': 'категории',
#         'object_list': ProductCat.objects.all(),
#     }
#     return render (request, 'kwadmin/productcat_list.html', context)


class CategoryList (SuperUserCheckMixin, HTMLTitleMixin, ListView):
    page_title = 'категории'
    model = ProductCat
    # template_name = 'kwadmin/productcat_list.html' - ищем сдесь шаблон
    # context_object_name = '...'               - рендерим другую переменную списка


class CategoryCreate(SuperUserCheckMixin, HTMLTitleMixin, CreateView):
    page_title = 'создание категории'
    model = ProductCat
    success_url = reverse_lazy('kwadmin:index')
    fields = '__all__'


