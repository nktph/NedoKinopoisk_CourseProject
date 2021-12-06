from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from django.db.models.aggregates import Avg


#1 Статья
GROUPS = [
    ('Книги','Книги'),
    ('Игры','Игры'),
    ('Фильмы','Фильмы'),
]

MARKS = [
    (1,'1 - Отвратительно'),
    (2,'2 - Ужасно'),
    (3,'3 - Плохо'),
    (4,'4 - Удовлетворительно'),
    (5,'5 - Нормально'),
    (6,'6 - Хорошо'),
    (7,'7 - Очень хорошо'),
    (8,'8 - Замечательно'),
    (9,'9 - Прекрасно'),
    (10,'10 - Шедеврально'),
]

class Article(models.Model):
    author_name = models.CharField('Имя автора', max_length = 50)
    article_title = models.CharField('Название статьи', max_length = 200)
    article_text = HTMLField('Текст статьи')
    pub_date = models.DateTimeField('Дата публикации')
    likes = models.PositiveIntegerField('Количество лайков', default=0)
    tags = TaggableManager()
    group = models.CharField('Категория',choices=GROUPS, max_length=6, default='')
    author_mark = models.PositiveSmallIntegerField('Оценка автора', choices=MARKS, default=0, blank=False)

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))

    def avg_rating(self, mode=1):
        ratings = Rating.objects.filter(article=self)
        ratings_avg = ratings.aggregate(Avg('rate')).get('rate__avg')
        ratings_count = ratings.count()
        if mode==1:
            return ratings_avg
        elif mode==2:
            return ratings_avg, ratings_count

    def best(self):
        return self.avg_rating()>=4.5

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


#2 Рейтинг
RATE_CHOISES = [
    (1, '1 - Ужасно'),
    (2, '2 - Плохо'),
    (3, '3 - Нормально'),
    (4, '4 - Хорошо'),
    (5, '5 - Великолепно'),
]
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOISES)

    class Meta:
        verbose_name="Рейтинг"
        verbose_name_plural="Рейтинги"

    def __str__(self):
        return f'{self.article} - {self.rate}'


#3 Комментарии
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('Имя автора', max_length = 50)
    comment_text = models.CharField('Текст комментария', max_length = 300)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

#4 Лайки
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    type_like = models.PositiveSmallIntegerField(choices=[(0, 'Не лайкнуто'),
                                                            (1, 'Лайкнуто')],default=0)
    class Meta:
        verbose_name="Лайк"
        verbose_name_plural="Лайки"

class Theme(models.Model):
    color = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user