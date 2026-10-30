from django.shortcuts import render
from django.http.response import HttpResponse
from articles.models import Article
# Create your views here.


def hello_world(request):
    return HttpResponse("<h1>Hello World</h1>")

def hello_name (request, name):
    return HttpResponse(f"Hello <h1>{name}</h1>")

def about_me_view(request):
    return HttpResponse("<h1>Привет!!!</h1>")

def articles_list(request):
    articles = Article.objects.all()
    text = "<h1>"
    return HttpResponse(articles)