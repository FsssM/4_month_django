from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Catalog, Comment


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"

    def get_queryset(self):
        queryset = super().get_queryset()
        if search := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search)
        return queryset


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/create.html"
    success_url = reverse_lazy("article_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/edit.html"
    pk_url_kwarg = "id"

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Это не ваш пост!")
        return redirect("article_detail", id=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"id": self.object.id})


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "articles/delete.html"
    context_object_name = "article"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Это не ваш пост!")
        return redirect("article_detail", id=self.kwargs["id"])


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("article_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("article_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Добро пожаловать! Аккаунт создан.")
        return response


class MyArticlesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


class HomeworkOneView(TemplateView):
    template_name = "articles/homework_one.html"


class CatalogListView(ListView):
    model = Catalog
    template_name = "articles/catalog_list.html"
    context_object_name = "catalogs"


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, id):
        article = get_object_or_404(Article, id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect("article_detail", id=article.id)
        return render(request, "articles/detail.html", {"article": article, "form": form})

    def get(self, request, id):
        return redirect("article_detail", id=id)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "articles/comment_edit.html"
    context_object_name = "comment"
    pk_url_kwarg = "id"

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Это не ваш комментарий!")
        return redirect("article_detail", id=self.get_object().article.id)

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"id": self.object.article.id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "articles/comment_delete.html"
    context_object_name = "comment"
    pk_url_kwarg = "id"

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Это не ваш комментарий!")
        return redirect("article_detail", id=self.get_object().article.id)

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"id": self.object.article.id})


class MyCommentsView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "articles/my_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
