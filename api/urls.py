from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from django.conf import settings
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="ScreenRecorder",
        default_version="v1",
        description="ScreenRecorder",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("", include("videos.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
