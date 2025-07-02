from rest_framework.routers import DefaultRouter
from media_assets.views import MediaAssetViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"media-assets", MediaAssetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
