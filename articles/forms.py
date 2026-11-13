from django import forms

from articles.models import Article

from .models import Comment
# class ArticleForm(forms.Form):
#     title = forms.CharField(min_length=5, max_length=100)
#     text = forms.Textarea()
#     rate = forms.IntegerField(min_value=0, max_value=10)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "text", "rate", "image", "category")

    def validation_title(self, title):
        if len(title) > 10:
            raise forms.ValidationError("validation error from func")

    def clean_title(self):
        title = self.cleaned_data["title"]

        if title == "NOT VALID":
            raise forms.ValidationError("TUT")

        self.validation_title(title)

        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "text"]
        widgets = {
            "author_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Текст комментария"}),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "").strip()
        if len(text) < 5:
            raise forms.ValidationError("Комментарий должен быть минимум из 5 символов!")
        
        banned_words = ["спам", "наркотики", "реклама"]
        for word in banned_words:
            if word in text.lower():
                raise forms.ValidationError(f"Слово «{word}» запрещено!")
        return text

    def clean_author_name(self):
        author = self.cleaned_data.get("author_name", "").strip()
        if author.isdigit():
            raise forms.ValidationError("Имя не может состоять только из цифр!")
        return author
