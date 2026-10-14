from django.contrib import admin
from django.urls import include, path
from voting import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("voting/", include("voting.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

# Keep your existing urlpatterns above.

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )