from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from K import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('directory/', include('directory.urls', namespace='directory')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
