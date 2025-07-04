from django.urls import include, path
from rest_framework.routers import DefaultRouter

from media_assets.views import MediaAssetViewSet

router = DefaultRouter()
router.register(r"media-assets", MediaAssetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
