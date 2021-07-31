"""Symfall URL Configuration

The `urlpatterns` list routes URLs to views.
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from authentication import views as authentication_views
from messenger import views as messenger_views

SchemaView = get_schema_view(
    openapi.Info(
        title="Symfall API",
        default_version="v1",
        description="API of the Symfall messenger",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="valeriiduz@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(
    r"auth",
    authentication_views.AuthViewSet,
    basename="auth",
)

router.register(r"users", messenger_views.UserViewSet, basename="user")
router.register(r"chat", messenger_views.ChatViewSet, basename="chat")
router.register(
    r"message",
    messenger_views.MessageViewSet,
    basename="message",
)
router.register(r"file", messenger_views.FileViewSet, basename="file")


def trigger_error(request):
    """
    Sentry Test function with ZeroDivisionError
    """
    return request, 1 / 0


urlpatterns = [
    path("sentry-debug/", trigger_error),
    path("admin/", admin.site.urls),
    path(
        "api-auth/",
        include(
            "rest_framework.urls",
            namespace="rest_framework",
        ),
    ),
    re_path(r"^health_check", include("health_check.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        SchemaView.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    re_path("^api/", include((router.urls, "api"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
