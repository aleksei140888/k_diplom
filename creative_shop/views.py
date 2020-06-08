import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from creative_shop.models import Shop, Product, DeliveryMethod, Card, CardItem, ActiveDeliveryMethods
from live_portal.utils import to_dict_list, MobileResponse
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


def product(request, product_id):
    product_obj = Product.objects.filter(id=product_id).first()
    delivery_methods = DeliveryMethod.objects.all()

    if not product_obj:
        return redirect('home_page')

    return render(request, 'shop_product.html', context={'product': product_obj, 'delivery_methods': delivery_methods})


def card(request, card_id):

    card_obj = Card.objects.filter(id=card_id).filter(status_id=1).first()
    active_methods = ActiveDeliveryMethods.objects.filter(shop_id=card_obj.shop.id).all()
    if not card_obj:
        return redirect('home_page')

    sum = 0
    for card_item in card_obj.products.all():
        sum += card_item.item.new_price

    return render(request, 'shop_card.html', context={'card': card_obj.to_dict(), 'delivery_methods': active_methods, 'price_sum': sum})


def card_add_item(request):
    resp = MobileResponse()
    data = json.loads(request.body.decode('utf-8'))

    fields = ['shop_id', 'product_id', 'product_count']
    for field in fields:
        if field not in data:
            resp.add_error('form/fields', f'В запросе отсутвует поле - {field}')

    if len(resp.raw['errors']):
        return resp.return_error()

    card = Card.objects.filter(user_id=request.user.id, shop_id=data['shop_id'], status_id=1).first()
    if not card:
        card = Card.objects.create(user_id=request.user.id, shop_id=data['shop_id'], status_id=1)

    item = CardItem.objects.filter(card_id=card.id, item_id=data['product_id']).first()
    if not item:
        item = CardItem.objects.create(card_id=card.id, item_id=data['product_id'], count=data['product_count'])
    else:
        item.count += int(data['product_count'])
        item.save()

    return HttpResponse(resp.return_success())
