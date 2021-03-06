from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from accounts.models import User

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    allUser = User.objects.all()
    form = CommentForm()
    context = {
        'articles': articles,
        'allUser': allUser,
        'form' : form
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form' : form
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article' : article,
        'form' : form
    }
    return render(request, 'articles/detail.html', context)

@require_POST
@login_required
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('accounts:profile', article.user.username)

def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form' : form
    }
    return render(request, 'articles/form.html', context)


def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user.is_authenticated:
        if request.user in article.like_users.all():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect('articles:index')
    else:
        return HttpResponse(status=401)

@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
                return redirect('articles:detail', article_pk)
    else:
        messages.warning(request, '해당 기능은 로그인이 필요합니다.')
        return redirect('accounts:login')

def comments(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article' : article,
        'form' : form,
    }
    return render(request, 'articles/comment.html', context)