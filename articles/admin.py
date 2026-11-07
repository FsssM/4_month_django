from django.contrib import admin

from articles.models import Article, Category

from .models import Catalog
# Register your models here.


admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Catalog)
