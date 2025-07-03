from rest_framework import serializers
from .models import MediaAsset


class MediaAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = [
            "id",
            "name",
            "slug",
            "file",
            "tags",
            "author",
            "license",
            "license_url",
            "license_type",
            "alt_text",
            "description",
            "is_active",
            "upload_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("slug", "created_at", "updated_at", "upload_at")

    def validate_file(self, value):
        """
        Ensure that the uploaded file is not empty and has a name.
        """
        if not value:
            raise serializers.ValidationError("File is required.")
        if not hasattr(value, "name") or not value.name:
            raise serializers.ValidationError("File must have a name.")
        return value
