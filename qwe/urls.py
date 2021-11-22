from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from filebrowser.sites import site

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/filebrowser/', site.urls),
    path('articles/', include('articles.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
