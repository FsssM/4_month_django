from django.http.request import HttpRequest
from django.shortcuts import render
from django.http.response import HttpResponse
from articles.models import Article, Catalog
# Create your views here.


def hello_world(request):
    return HttpResponse("<h1>Hello World</h1>")

def hello_name (request, name):
    return HttpResponse(f"Hello <h1>{name}</h1>")

def about_me_view(request):
    return HttpResponse("<h1>Привет!!!</h1>")

def articles_list(request: HttpRequest) -> HttpResponse:
    count: int = Article.objects.all().count()
    text = "<h1>"
    for i in range(1, count + 1):
        article = Article.objects.filter(id=i).first()
        text += f"{article.title} </h1><br><h1>"
    return HttpResponse(text)

from django.views.generic import ListView

class CatalogListView(ListView):
    model = Catalog
    template_name = 'articles/catalog_list.html'
    context_object_name = 'catalogs'
