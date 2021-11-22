from django.contrib import admin
from articles.models import Article, Comment

# admin.site.register(Article)
admin.site.register(Comment)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'author_name', 'pub_date')
    list_filter = ("pub_date",)
    search_fields = ['article_title', 'article_text']

admin.site.register(Article, ArticleAdmin)