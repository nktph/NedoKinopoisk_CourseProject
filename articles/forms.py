from django import forms
from .models import Article, Rating, RATE_CHOISES

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('article_title', 'group', 'article_text', 'author_mark', 'tags')

class RatingForm(forms.ModelForm):
    rate = forms.ChoiceField(choices=RATE_CHOISES, widget=forms.Select(), required=True)

    class Meta:
        model=Rating
        fields=('rate',)

