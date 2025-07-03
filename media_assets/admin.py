from django.contrib import admin
from .models import MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "file",
        "tags",
        "author",
        "upload_at",
        "license_type",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug", "tags", "author")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("is_active", "license_type")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "slug", "file", "tags", "author")}),
        ("License Information", {"fields": ("license_type", "license_url")}),
        ("Metadata", {"fields": ("alt_text", "description")}),
        ("Status", {"fields": ("is_active",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
