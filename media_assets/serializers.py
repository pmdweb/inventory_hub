from rest_framework import serializers
from .models import MediaAsset

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')
