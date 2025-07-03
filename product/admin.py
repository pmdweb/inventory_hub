from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "category",
        "tags",
        "price",
        "is_active",
        "featured_image",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "slug", "category__name")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("is_active", "category")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "tags",
                    "description",
                    "price",
                    "is_active",
                )
            },
        ),
        ("Media Information", {"fields": ("featured_image",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


# Register your models here.
