from main.models import ProductCat


def catalog_menu(request):
    return {
        'catalog_menu': ProductCat.objects.all(),
    }