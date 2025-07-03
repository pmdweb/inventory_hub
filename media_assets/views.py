from rest_framework import viewsets
from .models import MediaAsset
from .serializers import MediaAssetSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class MediaAssetViewSet(viewsets.ModelViewSet):
    queryset = MediaAsset.objects.all()
    serializer_class = MediaAssetSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
