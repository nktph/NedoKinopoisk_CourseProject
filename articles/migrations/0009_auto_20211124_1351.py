# Generated by Django 3.2.9 on 2021-11-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Лайки'),
            preserve_default=False,
        ),
    ]
