from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "tags",
            "description",
            "price",
            "is_active",
            "featured_image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("slug", "created_at", "updated_at")

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Price must be greater than or equal to 0."
            )
        return value
