from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

# Create your views here.
from creative_blog.models import MasterClass
from creative_shop.models import Shop, Product
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
    print(users)
    context = {
        'users': users,
        'shops': shops,
        'products': products,
        'mcs': mcs_dict,
        'card_products_count': request.user.cards.first().products.count() if request.user.is_authenticated and request.user.cards.first() and request.user.cards.first().products.first() else '0'
    }
    return render(request, 'home_page.html', context=context)


@login_required(login_url='/auth/signin/')
def user_page(request, user_id):
    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect('home_page')

    return render(request, 'account/user_page.html', context={'user': user.to_dict()})


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
            return HttpResponseBadRequest({'error': 'Пользователь уже существует'})

        new_user = User.objects.create(
            email=request.POST['email'],
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
        )

        new_user.set_password(request.POST['password'])
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
