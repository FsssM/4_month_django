from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from articles.views import (
    AddCommentView,
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    CatalogListView,
    CommentDeleteView,
    CommentUpdateView,
    HomeworkOneView,
    MyArticlesView,
    MyCommentsView,
    SignUpView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ArticleListView.as_view(), name="article_list"),
    path("my_articles/", MyArticlesView.as_view(), name="my_articles"),
    path("<int:id>/detail", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:id>/edit", ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:id>/delete", ArticleDeleteView.as_view(), name="article_delete"),
    path("create", ArticleCreateView.as_view(), name="article_create"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("homework1/", HomeworkOneView.as_view(), name="homework_one"),
    path("catalog/", CatalogListView.as_view(), name="catalog_list"),
    path("articles/<int:id>/comment/", AddCommentView.as_view(), name="add_comment"),
    path("comments/<int:id>/edit/", CommentUpdateView.as_view(), name="comment_edit"),
    path("comments/<int:id>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
    path("my-comments/", MyCommentsView.as_view(), name="my_comments"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
