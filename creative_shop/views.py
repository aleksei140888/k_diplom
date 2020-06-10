import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from creative_shop.models import Shop, Product, DeliveryMethod, Card, CardItem, ActiveDeliveryMethods
from live_portal import settings
from live_portal.utils import to_dict_list, MobileResponse
from main_site.models import User
from cloudipsp import Api, Checkout


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


def make_shop(request):
    resp = MobileResponse()
    if request.user.shops.first():
        return redirect('home_page')

    data = json.loads(request.body.decode('utf-8'))

    Shop.objects.create(name=data['name'], description=data['description'], rating=5, owner_id=request.user.id)

    return HttpResponse(resp.return_success())


def product(request, product_id):
    product_obj = Product.objects.filter(id=product_id).first()
    delivery_methods = DeliveryMethod.objects.all()

    if not product_obj:
        return redirect('home_page')

    return render(request, 'shop_product.html', context={'product': product_obj, 'delivery_methods': delivery_methods})


def card(request, card_id):

    card_obj = Card.objects.filter(id=card_id).filter(status_id=1).first()

    if not card_obj:
        return redirect('home_page')

    active_methods = ActiveDeliveryMethods.objects.filter(shop_id=card_obj.shop.id).all()

    context = {
        'card': card_obj.to_dict(),
        'delivery_methods': active_methods,
        'price_sum': card_obj.get_amount,
    }

    return render(request, 'shop_card.html', context=context)


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


def payment_make(request):
    resp = MobileResponse()

    data = json.loads(request.body.decode('utf-8'))

    card_obj = request.user.cards.filter(status_id=1).first()
    card_obj.delivery_method = DeliveryMethod.objects.filter(price=int(data['delivery_method'].split(',')[0])).first()
    amount = card_obj.get_amount()

    api = Api(merchant_id=settings.MERCHANT_ID,
              secret_key=settings.MERCHANT_SECRET_KEY)

    checkout = Checkout(api=api)

    data = {
        "currency": "UAH",
        "amount": int(amount*100)
    }

    url = checkout.url(data).get('checkout_url')
    resp.set_response(url)

    return HttpResponse(resp.return_success())


def success_payment(request):

    card = request.user.cards.filter(status_id=1).first()
    card.status_id = 2
    card.save()

    return render(request, 'success_payment.html')


def error_payment(request):

    return render(request, 'error_payment.html')
