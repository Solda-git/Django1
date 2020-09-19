from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from kwadmin.forms import KWAdminUserCreateForm, KWAdminUserUpdateForm, KWAdminCatCreateForm, KWAdminProductUpdateForm
from main.models import ProductCat, Product


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
    success_url = reverse_lazy('kwadmin:category_list')
    # fields = '__all__'
    form_class = KWAdminCatCreateForm


class CategoryUpdate(SuperUserCheckMixin, HTMLTitleMixin, UpdateView):
    page_title = 'редактирование категории'
    model = ProductCat
    success_url = reverse_lazy('kwadmin:category_list')
    form_class = KWAdminCatCreateForm
    pk_url_kwarg = 'cat_pk'


class CategoryDelete(SuperUserCheckMixin, HTMLTitleMixin, DeleteView):
    page_title = 'удаление категории'
    model = ProductCat
    success_url = reverse_lazy('kwadmin:category_list')
    pk_url_kwarg = 'cat_pk'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def category_products (request, cat_pk):
    category = get_object_or_404 (ProductCat, pk=cat_pk)
    object_list = category.product_set.all()
    context = {
        'title': f'категория {category.title}: продукты',
        'category': category,
        'object_list': object_list,
    }
    return render (request, 'kwadmin/category_products_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, cat_pk):
    category = get_object_or_404(ProductCat, pk=cat_pk)
    if request.method == 'POST':
        form = KWAdminProductUpdateForm (request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'kwadmin:category_products',
                kwargs={
                    'cat_pk': category.pk
                }
                # args=[cat_pk]
            ))
    else:
        form = KWAdminProductUpdateForm (
            initial = {
                'category': category,
            }
        )
        context = {
            'title': 'создание продукта',
            'form': form,
            'category': category,
        }
        return render(request, 'kwadmin/product_update.html', context)


# class ProductDetail(DetailView):
#     # page_title = 'удаление категории'
#     model = Product
#     pk_url_kwarg = 'product_pk'


def product_update (request, pk):
    title = 'продукт/редактирование'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = KWAdminProductUpdateForm (request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect (reverse (
                'kwadmin:category_products',
                kwargs={
                    'cat_pk': product.category.pk
                }
            ))
    else:
        form = KWAdminProductUpdateForm (instance=product)
        context = {
            'title': title,
            'form': form,
            'category': product.category
        }
        return render(request, 'kwadmin/product_update.html', context)


def product_delete (request, pk):
    title = 'продукт/удаление'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect (reverse (
                'kwadmin:category_products',
                kwargs={
                    'cat_pk': product.category.pk
                }
            ))
    content = {
        'title': title,
        'product': product
    }
    return render(request, 'kwadmin/product_delete.html' , content)