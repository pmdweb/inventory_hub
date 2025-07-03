from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class MediaAsset(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_("Media Asset Name")
    )
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name=_("Slug")
    )
    file = models.FileField(upload_to="media_library/", verbose_name=_("Media File"))
    tags = models.CharField(max_length=255, blank=True, verbose_name=_("Tags"))
    author = models.CharField(max_length=255, blank=True, verbose_name=_("Author"))
    upload_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Upload Date"))
    license = models.CharField(max_length=255, blank=True, verbose_name=_("License"))
    license_url = models.URLField(blank=True, verbose_name=_("License URL"))
    license_type = models.CharField(
        max_length=50,
        choices=[
            ("cc0", "CC0"),
            ("cc-by", "CC BY"),
            ("cc-by-sa", "CC BY-SA"),
            ("cc-by-nc", "CC BY-NC"),
            ("cc-by-nc-sa", "CC BY-NC-SA"),
            ("cc-by-nd", "CC BY-ND"),
            ("cc-by-nc-nd", "CC BY-NC-ND"),
        ],
        blank=True,
        null=True,
        verbose_name=_("License Type"),
    )
    alt_text = models.CharField(
        max_length=255, blank=True, verbose_name=_("Alternative Text")
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.license_type})" if self.license_type else self.name

    class Meta:
        verbose_name = _("Media Asset")
        verbose_name_plural = _("Media Assets")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["license_type"]),
            models.Index(fields=["upload_at"]),
        ]
