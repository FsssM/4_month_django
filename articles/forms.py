from django import forms

from articles.models import Article

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