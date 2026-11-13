from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, View

from articles.forms import ArticleForm
from articles.models import Article, Catalog, Comment

def articles_list(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter()

    if search := request.GET.get("q"):
        articles = articles.filter(title__icontains=search)

    return render(request, "articles/list.html", {"articles": articles})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = get_object_or_404(Article, id=id)
    return render(request, "articles/detail.html", {"article": article})


@login_required
def article_create(request: HttpRequest) -> HttpResponse:
    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect("article_list")
    return render(request, "articles/create.html", {"form": form})


@login_required
def article_edit(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if article.user != request.user:
        messages.error(request, "Это не ваш пост!")
        return redirect("article_detail", id=article.pk)

    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=form.instance.id)

    return render(request, "articles/edit.html", {"form": form})


@login_required
def article_delete(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if article.user != request.user:
        messages.error(request, "Это не ваш пост!")
        return redirect("article_detail", id=article.pk)

    if request.method == "POST":
        article.delete()
        return redirect("article_list")

    return render(request, "articles/delete.html", context={"article": article})


def signup(request):
    if request.user.is_authenticated:
        return redirect("article_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Добро пожаловать! Аккаунт создан.")
            return redirect("article_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def my_articles(request: HttpRequest):
    articles = Article.objects.filter(user=request.user)
    return render(request, "articles/list.html", {"articles": articles})


# === ТВОИ ДОМАШКИ ЗА 1–4 УРОКИ ===

def homework_one_view(request):
    return render(request, "articles/homework_one.html")


class CatalogListView(ListView):
    model = Catalog
    template_name = 'articles/catalog_list.html'
    context_object_name = 'catalogs'


class AddCommentView(View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        author = request.POST.get('author_name')
        text = request.POST.get('text')
        
        if author and text:
            Comment.objects.create(article=article, author_name=author, text=text)
            
        return redirect('article_detail', pk=pk)
