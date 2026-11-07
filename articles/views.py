from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from articles.forms import ArticleForm
from articles.models import Article

from django.views.generic import ListView
from .models import Catalog

def articles_list(request: HttpRequest) -> HttpResponse:
    articles_list = Article.objects.all()

    return render(request, "articles/list.html", {"articles": articles_list})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    return render(request, "articles/detail.html", {"article": article})


def article_create(request: HttpRequest) -> HttpResponse:
    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_list")
    return render(request, "articles/create.html", {"form": form})


def article_edit(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=form.instance.id)

    return render(request, "articles/edit.html", {"form": form})


def article_delete(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if request.method == "POST":
        article.delete()
        return redirect("article_list")

    return render(request, "articles/delete.html", context={"article": article})


def homework_one_view(request):
    return render(request, "articles/homework_one.html")


class CatalogListView(ListView):
    model = Catalog
    template_name = 'articles/catalog_list.html'
    context_object_name = 'catalogs'
