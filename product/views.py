from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer

# from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
