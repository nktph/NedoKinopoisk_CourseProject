from django.contrib import admin
from articles.models import Article, Comment, Rating, Like, Theme

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'group', 'author_name', 'pub_date')
    list_filter = ("pub_date",)
    search_fields = ['article_title', 'article_text']
admin.site.register(Article, ArticleAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'author_name')
    list_filter = ('author_name',)
    search_fields = ['author_name', 'comment_text']
admin.site.register(Comment, CommentAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('article', 'rate', 'user')
    list_filter = ('rate',)
    search_fields = ['article', 'user']
admin.site.register(Rating, RatingAdmin)

admin.site.register(Like)
admin.site.register(Theme)


