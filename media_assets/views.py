from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.authentication import TokenAuthentication
from .models import MediaAsset
from .serializers import MediaAssetSerializer

class MediaAssetViewSet(viewsets.ModelViewSet):
    queryset = MediaAsset.objects.all()
    serializer_class = MediaAssetSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
# Create your views here.
