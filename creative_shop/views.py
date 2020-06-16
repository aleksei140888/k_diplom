import json
import time
from hashlib import md5

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import date

from creative_shop.models import Shop, Product, DeliveryMethod, Card, CardItem, ActiveDeliveryMethods
from live_portal import settings
from live_portal.utils import to_dict_list, MobileResponse, activity
from main_site.models import User, ActivityLog
from cloudipsp import Api, Checkout


def all_shops(request):
    activity(request)

    shop_objects = Shop.objects.all()

    if not shop_objects:
        return redirect('home_page')

    paginator = Paginator(shop_objects, 8)
    page = request.GET.get('page')

    try:
        shops = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        shops = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        shops = paginator.page(paginator.num_pages)

    return render(request, 'shop_all_shops.html', context={'page': page, 'shops': shops})


def shop(request, shop_id):
    activity(request)

    shop_obj = Shop.objects.filter(id=shop_id).first()
    products = to_dict_list(Product.objects.filter(shop_id=shop_id).all())

    paginator = Paginator(products, 8)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop_shop.html', context={'shop': shop_obj, 'products': products})


def make_shop(request):
    resp = MobileResponse()
    if request.user.shops.first():
        return redirect('home_page')

    data = json.loads(request.body.decode('utf-8'))

    shop = Shop.objects.create(name=data['name'], description=data['description'], rating=5, owner_id=request.user.id)

    for method in DeliveryMethod.objects.all():
        ActiveDeliveryMethods.objects.create(shop_id=shop.id, delivery_method_id=method.id)

    return HttpResponse(resp.return_success())


def product(request, product_id):
    activity(request)

    product_obj = Product.objects.filter(id=product_id).first()
    delivery_methods = DeliveryMethod.objects.all()

    if not product_obj:
        return redirect('home_page')

    return render(request, 'shop_product.html', context={'product': product_obj, 'delivery_methods': delivery_methods})


def card(request, card_id):
    activity(request)

    card_obj = Card.objects.filter(user_id=card_id).filter(status_id=1).first()

    if not card_obj or not card_obj.products.all():
        return redirect('home_page')

    active_methods = ActiveDeliveryMethods.objects.filter(shop_id=card_obj.shop.id).all()

    context = {
        'card': card_obj.to_dict(),
        'delivery_methods': active_methods,
        'price_sum': card_obj.get_amount,
    }

    return render(request, 'shop_card.html', context=context)


@login_required(login_url='/auth/')
def card_item(request):
    resp = MobileResponse()
    if request.method == "POST":
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
    elif request.method == "DELETE":
        data = json.loads(request.body.decode('utf-8'))

        item = CardItem.objects.filter(card__user_id=request.user.id, item_id=data['card_item_id']).first()
        item.delete()

        resp.set_response(data['card_item_id'])

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

    order_str = f"{request.user.username}_{time.time()}"

    data = {
        "order_id": order_str,
        "currency": "UAH",
        "amount": int(amount*100)
    }

    url = checkout.url(data).get('checkout_url')
    resp.set_response(url)

    return HttpResponse(resp.return_success())


def success_payment(request):
    activity(request)

    card = request.user.cards.filter(status_id=1).first()
    card.status_id = 2
    card.save()

    return render(request, 'success_payment.html')


def error_payment(request):
    activity(request)

    return render(request, 'error_payment.html')


def shop_set_in_delivery_status(request, card_item_id):
    card_item = CardItem.objects.filter(id=card_item_id).first()
    if card_item:
        card_item.card.status_id = 3
        card_item.card.save()

    return redirect(reverse('user_page', args=[request.user.id]))


def shop_set_in_completed_status(request, card_item_id):
    card_item = CardItem.objects.filter(id=card_item_id).first()
    if card_item:
        card_item.card.status_id = 4
        card_item.card.save()

    return redirect(reverse('user_page', args=[request.user.id]))


def shop_get_owner_cards(request):
    if not request.user or not request.user.shops.first() or request.user.shops.first().cards.all():
        return HttpResponse(json.dumps({'data': []}))

    cards = request.user.shops.first().cards.all()
    products_dict = {'data': []}
    for card in cards:
        for item in card.products.all():
            button = ''
            if card.status.id == 2:
                button = f'<a href="{reverse("shop_set_in_delivery_status", args=[item.id])}" style="margin-left: 10px;"><button class="btn btn-warning" title="В процессе доставки"><i class="fa fa-check"></i></button></a>'
            elif card.status.id == 3:
                button = f'<a href="{reverse("shop_set_in_completed_status", args=[item.id])}" style="margin-left: 10px;"><button class="btn btn-warning" title="Выполнено"><i class="fa fa-check"></i></button></a>'
            products_dict['data'].append([
                item.card.id,
                item.item.name,
                str(item.item.new_price),
                card.user.first_name + ' ' + card.user.last_name,
                str(card.user.phone_number),
                card.delivery_method.name,
                card.status.name_ru,
                button,
            ])
    return HttpResponse(json.dumps(products_dict))


def shop_get_owner_products(request):
    products = request.user.shops.first().products.all()
    products_dict = {'data': []}
    for product in products:
        products_dict['data'].append([
            product.id,
            product.name,
            product.category.name,
            str(product.old_price),
            str(product.new_price),
            str(product.rating),
            f'<button class="btn btn-warning" onclick="window.open({reverse("edit_product_window", args=[product.id])})"><i class="fa fa-pencil"></i></button>'
            f'<a href="{reverse("delete_product", args=[product.id])}" style="margin-left: 10px;"><button class="btn btn-danger"><i class="fa fa-trash"></i></button></a>',
        ])
    return HttpResponse(json.dumps(products_dict))


def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product or product.shop.owner_id != request.user.id:
        return redirect('home_page')
    for card_item in product.products.all():
        if card_item.card.status_id == 1:
            card_item.delete()
    product.delete()

    return redirect(reverse('user_page', args=[request.user.id]))


def add_product(request):
    data = request.POST
    product = Product.objects.create(
        name=data['name'],
        description=data['description'],
        old_price=data['new_price'],
        new_price=data['new_price'],
        category_id=data['category_id'],
        photo_filename=request.FILES['file'],
        shop_id=request.user.shops.first().id,
        rating=5,
    )
    return redirect(reverse('user_page', args=[request.user.id]))


def edit_product(request):
    data = request.POST
    product = Product.objects.filter(id=data['id'])(
        name=data['name'],
        description=data['description'],
        old_price=data['new_price'],
        new_price=data['new_price'],
        category_id=data['category_id'],
        photo_filename=request.FILES['file'],
    )
    return HttpResponse()


def edit_product_window(request, product_id):
    activity(request)

    product_obj = Product.objects.filter(id=product_id).first()
    return render(request, 'window_edit_product.html', context={'product': product_obj})


def shop_get_pursaches(request):
    if not request.user or not request.user.cards.all():
        return HttpResponse(json.dumps({'data': []}))
    pursaches = request.user.cards.all()
    products_dict = {'data': []}
    for card in pursaches:
        for card_item in card.products.all():
            products_dict['data'].append([
                card.id,
                card_item.item.name,
                str(card_item.item.new_price),
                card.delivery_method.name if card.delivery_method else 'Требует уточнения',
                card.status.name_ru,
            ])
    return HttpResponse(json.dumps(products_dict))
