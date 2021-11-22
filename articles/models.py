from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField

#1 Статья
class Article(models.Model):
    author_name = models.CharField('Имя автора', max_length = 50)
    article_title = models.CharField('Название статьи', max_length = 200)
    article_text = HTMLField('Текст статьи')
    pub_date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('Имя автора', max_length = 50)
    comment_text = models.CharField('Текст комментария', max_length = 300)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

#2 Рейтинг
#3 Комментарии
