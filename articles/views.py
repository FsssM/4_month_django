from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.


def hello_world(request):
    return HttpResponse("<h1>Hello World</h1>")

def hello_name (request, name):
    return HttpResponse(f"Hello <h1>{name}</h1>")

def about_me_view(request):
    return HttpResponse("<h1>Привет!!!</h1>")