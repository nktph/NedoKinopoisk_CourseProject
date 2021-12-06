from django.contrib import admin
from django.urls import path, include
from filebrowser.sites import site
from articles.views import home, userprofile, theme
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('tinymce/', include('tinymce.urls')),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile', userprofile, name='userprofile'),
    path('theme', theme, name='theme'),
]

if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
