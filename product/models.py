from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from catalog.models import Category
from media_assets.models import MediaAsset


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Category")
    )
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Product Name"))
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name=_("Slug"))
    tags = models.CharField(max_length=255, blank=True, verbose_name=_("Tags"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    featured_image = models.ForeignKey(
        MediaAsset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="featured_in_products",
        verbose_name=_("Featured Image")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["price"]),
        ]
