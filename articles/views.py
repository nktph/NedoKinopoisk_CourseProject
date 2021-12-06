from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Rating, Like, Comment, Theme
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import ArticleForm, RatingForm
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag


def home(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    best = Article.objects.order_by('-likes')[:3]
    tags = Tag.objects.all()

    if not request.user.is_authenticated:
        color = 'light'
        return render(request, 'base.html', {'latest_articles_list': latest_articles_list,
                                             'best': best,
                                             'tags': tags,
                                             'color': color})

    elif Theme.objects.filter(user=request.user).exists():
        color=Theme.objects.get(user=request.user).color
    else:
        color='light'
    return render(request, 'base.html', {'latest_articles_list': latest_articles_list,
                                         'best':best,
                                         'tags':tags,
                                         'color':color})

def userprofile(request):
    if request.user.is_superuser:
        article_list = Article.objects.all()
    else:
        article_list = Article.objects.filter(author_name=request.user.username)
    likes_count=0
    for a in article_list:
        likes_count+=a.likes

    if not request.user.is_authenticated:
        color = 'light'
    elif Theme.objects.filter(user=request.user).exists():
        color=Theme.objects.get(user=request.user).color
    else:
        color='light'

    return render(request, 'account/userprofile.html', {'article_list': article_list,
                                                        'likes_count':likes_count,
                                                        'color':color})

def index(request):
    articles_list = Article.objects.order_by('-pub_date')
    if not request.user.is_authenticated:
        color = 'light'
    elif Theme.objects.filter(user=request.user).exists():
        color=Theme.objects.get(user=request.user).color
    else:
        color='light'
    return render(request, 'articles/list.html', {'articles_list': articles_list,
                                                  'color':color})

def detail(request, article_id, form=0):
    try:
        a = Article.objects.get(id = article_id)
    except:
        raise Http404("Статья не найдена!")
    latest_comment_list = a.comment_set.order_by('-id')

    ratings_avg, ratings_count = a.avg_rating(2)
    group = a.group
    form = RatingForm()

    if not request.user.is_authenticated:
        color = 'light'
    elif Theme.objects.filter(user=request.user).exists():
        color=Theme.objects.get(user=request.user).color
    else:
        color='light'

    return render(request, 'articles/detail.html', {'article': a,
                                                    'latest_comment_list': latest_comment_list,
                                                    'ratings_avg':ratings_avg,
                                                    'ratings_count':ratings_count,
                                                    'form':form,
                                                    'group':group,
                                                    'color':color})



def like(request, article_id):
    user_liking = request.user
    article = Article.objects.get(id=article_id)
    current_likes = article.likes

    liked = Like.objects.filter(user=user_liking, article=article, type_like=1).count()

    if not liked:
        like = Like.objects.create(user=user_liking, article=article, type_like=1)
        current_likes+=1
    else:
        Like.objects.filter(user=user_liking, article=article, type_like=1 ).delete()
        current_likes-=1

    article.likes = current_likes
    article.save()

    return HttpResponseRedirect( reverse('articles:detail', args=(article.id,)) )

def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except:
        raise Http404("Статья не найдена!")

    a.comment_set.create(author_name=request.user.username, comment_text=request.POST['text'])
    return HttpResponseRedirect( reverse('articles:detail', args=(a.id,)) )

def rate(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except:
        raise Http404("Статья не найдена!")

    user = request.user
    r = Rating.objects.filter(user=user, article=article)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            if r:
                r.delete()
            rate = form.save(commit=False)
            rate.user = user
            rate.article = article
            rate.save()
    else: return Http404("Что-то пошло не так")

    return HttpResponseRedirect( reverse('articles:detail', args=(article.id,)) )

def new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_name = request.user.username
            article.pub_date = timezone.now()
            article.save()
            form.save_m2m()
            return HttpResponseRedirect( reverse('articles:detail', args=(article.id,)) )
    else:
        form = ArticleForm()

    if Theme.objects.filter(user=request.user).exists():
        color=Theme.objects.get(user=request.user).color
    else:
        color='light'
    return render(request, 'articles/edit.html', {'form': form,
                                                  'color':color})

def edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.pub_date = timezone.now()
            article.save()
            form.save_m2m()
            return HttpResponseRedirect( reverse('articles:detail', args=(article.id,)) )
    else:
        form = ArticleForm(instance=article)

    if Theme.objects.filter(user=request.user).exists():
        color=Theme.objects.get(user=request.user).color
    else:
        color='light'
    return render(request, 'articles/edit.html', {'form': form,
                                                  'color':color})

def delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return userprofile(request)

def search(request):
    if not request.user.is_authenticated:
        color = 'light'
    elif Theme.objects.filter(user=request.user).exists():
        color = Theme.objects.get(user=request.user).color
    else:
        color = 'light'
    if request.method == "POST":
        searched = request.POST.get('searched')

        articles = Article.objects.annotate(search=SearchVector('article_title')).filter(search=str(searched))

        text = Article.objects.annotate(search=SearchVector('article_text')).filter(search=str(searched))

        comments = Comment.objects.annotate(search=SearchVector('comment_text')).filter(search=str(searched))

        # articles = Article.objects.annotate(similarity = TrigramSimilarity('article_title', searched),).filter(
        #     similarity__gt=0.1).order_by('-similarity')
        # text = Article.objects.annotate(search=SearchVector('article_text')).filter(search=searched)
        # comments = Comment.objects.annotate(similarity=TrigramSimilarity('comment_text', searched), ).filter(
        #     similarity__gt=0.1).order_by('-similarity')

        tags = Article.objects.filter(tags__name__in=[searched])



        return render(request, 'articles/search.html', {'searched':searched, 'in_articles':articles,
                                                        'in_text':text, 'in_tags':tags,
                                                        'in_comments':comments, 'color':color})
    else:
        return render(request, 'articles/search.html', {'color':color})

def bytags(request, tag_id):
    tag = get_object_or_404(Tag,id=tag_id)
    articles = Article.objects.filter(tags__name__in=[tag.name])
    if not request.user.is_authenticated:
        color = 'light'
    elif Theme.objects.filter(user=request.user).exists():
        color=Theme.objects.get(user=request.user).color
    else:
        color='light'
    return render(request, 'articles/bytags.html',{'articles': articles,
                                                   'tagname':tag.name,
                                                   'color':color})


def theme(request):
    color = request.GET.get('color')
    if color == 'dark':
        if Theme.objects.filter(user=request.user).exists():
            user_theme = Theme.objects.get(user=request.user)
            user_theme.user = request.user
            user_theme.color = 'secondary'
            user_theme.save()
        else:
            user2=Theme(user=request.user, color='secondary')
            user2.save()
    elif color == 'light':
        if Theme.objects.filter(user=request.user).exists():
            user_theme1 = Theme.objects.get(user=request.user)
            user_theme1.user = request.user
            user_theme1.color = 'light'
            user_theme1.save()
        else:
            user4=Theme(user=request.user, color='light')
            user4.save()

    return redirect('/')