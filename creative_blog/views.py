from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from creative_blog.models import MasterClass
from live_portal.utils import to_dict_list
from main_site.models import User


def all_blogs(request):
    blog_objects = MasterClass.objects.all()
    paginator = Paginator(blog_objects, 10)
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
    article = MasterClass.objects.filter(id=article_id).first()

    if not article:
        return redirect('home_page')

    return render(request, 'article.html', context={'article': article.to_dict_full()})
