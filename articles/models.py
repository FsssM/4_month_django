from django.contrib.auth.models import User

from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(null=True, upload_to="articles/")
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("-created_at",)


class Category(models.Model):
    name = models.CharField(max_length=100)

class Catalog(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} — {self.article.title}"
