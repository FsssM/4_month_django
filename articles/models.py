from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(null=True, upload_to="articles/")
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("-created_at",)


class Category(models.Model):
    name = models.CharField()