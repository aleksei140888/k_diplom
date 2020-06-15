import json
from random import randint

import requests
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

# Create your views here.
from creative_blog.models import MasterClass
from creative_shop.models import Shop, Product, ProductCategory
from live_portal import settings
from live_portal.utils import to_dict_list, MobileResponse, mobile_400, mobile_200
from main_site.models import User


def home_page(request):
    shops = Shop.objects.all().order_by('-rating')[:4]
    products = Product.objects.all().order_by('-rating')[:4]
    users = to_dict_list(User.objects.all().order_by('-rating')[:4])
    mcs = MasterClass.objects.all().order_by('?')[:4]
    mcs_dict = []
    for mc in mcs:
        mcs_dict.append(mc.to_dict())

    for user in users:
        user['profile_link'] = f'{request.build_absolute_uri()}user/{user["id"]}/'
    context = {
        'users': users,
        'shops': shops,
        'products': products,
        'mcs': mcs_dict,
        'card_products_count': request.user.cards.first().products.count() if request.user.is_authenticated and request.user.cards.first() and request.user.cards.first().products.first() else '0'
    }
    return render(request, 'home_page.html', context=context)


def get_card_items_count(request):
    ajax_resp = MobileResponse()
    ajax_resp.set_response({
            'card_products_count': request.user.cards.filter(status_id=1).first().products.count() if request.user.is_authenticated and
                                                                                  request.user.cards.filter(status_id=1).first() and
                                                                                  request.user.cards.filter(status_id=1).first().products.first() else '0'
        })
    return HttpResponse(ajax_resp.return_success())


@login_required(login_url='/auth/signin/')
def user_page(request, user_id):
    user = User.objects.filter(id=user_id).first()
    categories = ProductCategory.objects.all()
    if not user:
        return redirect('home_page')

    context = {
        'user': user.to_dict(),
        'categories': categories,
        'shop_exist': 1 if user.shops.first() else 0,
    }

    return render(request, 'account/user_page.html', context=context)


@login_required(login_url='/auth/signin/')
def load_profile(request):
    raw = MobileResponse()

    if request.user.is_authenticated and request.method == "GET":
        raw.set_response(request.user.to_dict())
        return mobile_200(raw.return_success())
    else:
        return mobile_400(raw.with_error(parameter=f"method/{request.method}",
                                         detail=f"Request method {request.method} does not support"))


@login_required(login_url='/auth/signin/')
def user(request, user_id):
    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect('home_page')

    return render(request, 'account/user.html', context={'user': user.to_dict()})


def all_users_page(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        users = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        users = paginator.page(paginator.num_pages)

    return render(request, 'account/all_users.html', context={'page_obj': page, 'users': users, 'users_dict': to_dict_list(users)})


def auth_page(request):
    if request.method == 'GET':
        return render(request, 'account/auth_page.html')
    else:
        return HttpResponseBadRequest()


def auth_register(request):
    if request.method == 'GET':
        return render(request, 'account/register.html')
    elif request.method == 'POST':
        user = User.objects.filter(email=request.POST['email']).filter(is_active=1).first()

        if user:
            return HttpResponseBadRequest({'Пользователь уже существует'})

        if request.POST['password'] != request.POST['confirm_password']:
            return HttpResponseBadRequest({'Пароли не совпадают'})

        new_user = User.objects.create(
            email=request.POST['email'],
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            phone_number=request.POST['phone_number'],
            phone_number_verify_code=request.POST['phone_number_code'],
            forum_nickname=request.POST['forum_nickname'],
        )

        new_user.set_password(request.POST['password'])

        new_user.save()

        return redirect('auth_page')
    else:
        pass


def auth_login(request):
    pass


def auth_sign(request):
    user = authenticate(username=request.GET['username'], password=request.GET['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('home_page')
        else:
            return redirect('auth_page')
    else:
        return redirect('auth_page')


def auth_signout(request):
    logout(request)
    return redirect('home_page')


def get_statistic(request):
    if request.method == "GET":
        return render(request, "account/admin/statistic.html")
    elif request.method == "POST":
        pass
    else:
        pass


def check_number(request):
    resp = MobileResponse()
    data = json.loads(request.body.decode('utf-8'))

    if 'phone_number' not in data:
        resp.add_error('request/data', 'Вы не ввели номер телефона')
        return HttpResponse(resp.return_error())

    code = randint(1000, 9999)

    try:
        ucaller_link = f'https://api.ucaller.ru/v1.0/initCall?service_id={settings.UCALLER_ID}&key={settings.UCALLER_SECRET_KEY}&phone={data["phone_number"]}&code={code}'
        ucaller_request = requests.get(ucaller_link)
    except Exception:
        resp.add_error('request/confirm', 'Произошла ошибка, возможно, вы не подключены к интернету или сервис не доступен.')
        return HttpResponse(resp.return_error())

    resp.set_response(code)

    return HttpResponse(resp.return_success())


def help_page(request):
    return render(request, 'help.html')

