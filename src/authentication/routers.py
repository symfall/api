from rest_framework.routers import DefaultRouter

from authentication.api.v1.views import AuthViewSet

router = DefaultRouter(trailing_slash=False)

router.register(
    prefix="auth",
    viewset=AuthViewSet,
    basename="auth",
)
