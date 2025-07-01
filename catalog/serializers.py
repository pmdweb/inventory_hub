from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')

    # def create(self, validated_data):
    #     category = Category.objects.create(**validated_data)
    #     return category

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.is_active = validated_data.get('is_active', instance.is_active)
    #     instance.save()
    #     return instance