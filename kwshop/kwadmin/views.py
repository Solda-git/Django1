from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


@user_passes_test (lambda u: u.is_superuser)
def index(request):
    object_list = get_user_model().objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': 'пользователи',
        'object_list': object_list,
    }
    return render(request, 'kwadmin/index.html', context)