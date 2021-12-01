from django.urls import path, include
from . import views


app_name = 'articles'
urlpatterns = [
    path('', views.index, name = "index"),
    path('<int:article_id>/', views.detail, name = "detail"),
    path('<int:article_id>/leave_comment/', views.leave_comment, name="leave_comment"),
    path('new/', views.new, name="new"),
    path('<int:article_id>/edit/', views.edit, name="edit"),
    path('<int:article_id>/rate/', views.rate, name="article-rate"),
    path('<int:article_id>/like/', views.like, name="article-like"),
    path('search/', views.search, name="search"),
    path('bytags/<int:tag_id>', views.bytags, name="bytags"),
]