import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from creative_blog.models import MasterClass, MasterClassPhoto, MasterClassVideo
from live_portal.utils import to_dict_list, activity
from main_site.models import User


def all_blogs(request):
    activity(request)

    blog_objects = MasterClass.objects.all()
    paginator = Paginator(blog_objects, 5)
    page = request.GET.get('page')

    try:
        mcs = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        mcs = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        mcs = paginator.page(paginator.num_pages)

    return render(request, 'all_creative_blogs.html', context={'page_obj': page, 'articles': mcs, 'mcs': to_dict_list(mcs)})


def blog(request, user_id):
    activity(request)

    blog_objects = MasterClass.objects.filter(author_id=user_id)
    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect('home_page')

    paginator = Paginator(blog_objects, 10)
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        articles = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        articles = paginator.page(paginator.num_pages)

    articles_dict = []
    for article_item in articles:
        articles_dict.append(article_item.to_dict())

    return render(request, 'blog.html', context={'page': page, 'articles': articles, 'articles_dict': articles_dict, 'user': user.to_dict()})


def article(request, article_id):
    activity(request)

    article = MasterClass.objects.filter(id=article_id).first()

    if not article:
        return redirect('home_page')

    return render(request, 'article.html', context={'article': article.to_dict_full()})


def blog_get_masterclasses(request):
    mcs = request.user.master_classes.all()

    products_dict = {'data': []}
    for mc in mcs:
        products_dict['data'].append([
            mc.id,
            mc.title,
            f'<button class="btn btn-warning" onclick="window.open({reverse("edit_master_class_window", args=[mc.id])})"><i class="fa fa-pencil"></i></button>'
            f'<a href="{reverse("article_delete", args=[mc.id])}" style="margin-left: 10px;"><button class="btn btn-danger"><i class="fa fa-trash"></i></button></a>',
        ])
    return HttpResponse(json.dumps(products_dict))


def delete_master_class(request, article_id):
    mc = MasterClass.objects.filter(article_id).first()
    mc.delete()
    return redirect(reverse('user_page', args=[request.user.id]))


def edit_master_class_window(request, article_id):
    activity(request)

    product_obj = MasterClass.objects.filter(id=article_id).first()
    return render(request, 'window_edit_product.html', context={'product': product_obj})


def article_create(request):

    data = request.POST
    article = MasterClass.objects.create(
        title=data['title'],
        text=data['text'],
        author_id=request.user.id
    )

    photo = MasterClassPhoto.objects.create(
        master_class_id=article.id,
        filename=request.FILES['photo_file2'],
        extension='jpg',
    )

    if 'video_file2' in request.FILES:
        video = MasterClassVideo.objects.create(
            master_class_id=article.id,
            filename=request.FILES['video_file2'],
            extension='mp4',
        )
    return redirect(reverse('user_page', args=[request.user.id]))


def article_delete(request, article_id):
    article = MasterClass.objects.filter(id=article_id).first()

    article.photo.all().delete() if article.photo.all() else ''
    article.video.all().delete() if article.video.all() else ''

    article.delete()

    return redirect(reverse('user_page', args=[request.user.id]))