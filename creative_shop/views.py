from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from creative_shop.models import Shop, Product
from live_portal.utils import to_dict_list
from main_site.models import User


def all_shops(request):
    shop_objects = Shop.objects.all()

    if not shop_objects:
        return redirect('home_page')

    paginator = Paginator(shop_objects, 10)
    page = request.GET.get('page')

    try:
        shops = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        shops = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        shops = paginator.page(paginator.num_pages)

    return render(request, 'shop_shop.html', context={'page': page, 'shops': shops})


def shop(request, shop_id):
    shop_obj = Shop.objects.filter(id=shop_id).first()
    products = to_dict_list(Product.objects.filter(shop_id=shop_id).all())

    return render(request, 'shop_shop.html', context={'shop': shop_obj, 'products': products})
