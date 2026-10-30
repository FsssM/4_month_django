from django.contrib import admin

# Register your models here.

from .models import Article, Catalog

admin.site.register(Article)
admin.site.register(Catalog)
