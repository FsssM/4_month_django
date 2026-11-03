from django.contrib import admin

from articles.models import Article, Category
# Register your models here.

from .models import Article, Catalog

admin.site.register(Article)
admin.site.register(Catalog)
