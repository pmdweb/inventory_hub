# Generated by Django 5.2.3 on 2025-07-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="category",
            index=models.Index(fields=["name"], name="catalog_cat_name_39f70b_idx"),
        ),
        migrations.AddIndex(
            model_name="category",
            index=models.Index(fields=["slug"], name="catalog_cat_slug_695af4_idx"),
        ),
    ]
