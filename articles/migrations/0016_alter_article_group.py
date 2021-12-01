# Generated by Django 3.2.9 on 2021-11-27 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_article_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='group',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Книги'), (1, 'Игры'), (3, 'Фильмы')], default=0, verbose_name='Категория'),
        ),
    ]