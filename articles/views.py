from django.shortcuts import render, get_object_or_404
from .models import Article
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import ArticleForm
from django.utils import timezone

def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:7]
    return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})

def detail(request, article_id):
    try:
        a = Article.objects.get(id = article_id)
    except:
        raise Http404("Статья не найдена!")

    latest_comment_list = a.comment_set.order_by('-id')

    return render(request, 'articles/detail.html', {'article': a, 'latest_comment_list': latest_comment_list})

def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except:
        raise Http404("Статья не найдена!")

    a.comment_set.create(author_name=request.user.username, comment_text=request.POST['text'])
    return HttpResponseRedirect( reverse('articles:detail', args=(a.id,)) )

def new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_name = request.user.username
            article.pub_date = timezone.now()
            article.save()
            return HttpResponseRedirect( reverse('articles:detail', args=(article.id,)) )
    else:
        form = ArticleForm()
    return render(request, 'articles/edit.html', {'form': form})

def edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.pub_date = timezone.now()
            article.save()
            return HttpResponseRedirect( reverse('articles:detail', args=(article.id,)) )
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit.html', {'form': form})