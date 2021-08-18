"""
Symfall URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from authentication.routers import router as authentication
from messenger.routers import router as messenger

SchemaView = get_schema_view(
    openapi.Info(
        title="Symfall API",
        default_version="v1",
        description="API of the Symfall messenger",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="valerii.duz@symfall.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def trigger_error(request):
    """
    Sentry Test function with ZeroDivisionError
    """
    return request, 1 / 0


urlpatterns = [
    path("sentry-debug/", trigger_error),
    path("health_check", include("health_check.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/",
        include((authentication.urls, "authentication")),
        name="api",
    ),
    path(
        "api/",
        include((messenger.urls, "messenger")),
        name="api",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
