import pytest
from catalog.models import Category
from catalog.serializers import CategorySerializer

# This test checks if the serializer creates a Category and auto-generates the slug correctly
@pytest.mark.django_db
def test_category_serializer_create():
    data = {"name": "Terrenos"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.slug == "terrenos"
    assert instance.name == "Terrenos"

# This test ensures the serializer rejects empty 'name' field
def test_serializer_rejects_empty_name():
    serializer = CategorySerializer(data={"name": ""})
    assert not serializer.is_valid()
    assert "name" in serializer.errors

# This test verifies that duplicate category names are not allowed
@pytest.mark.django_db
def test_serializer_rejects_duplicate_name():
    Category.objects.create(name="Terrenos")
    serializer = CategorySerializer(data={"name": "Terrenos"})
    assert not serializer.is_valid()
    assert "name" in serializer.errors

# This test checks if the serializer accepts a valid name and generates the correct slug
@pytest.mark.django_db
def test_serializer_accepts_valid_name():
    serializer = CategorySerializer(data={"name": "Terrenos Urbanos"})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Terrenos Urbanos"
    assert instance.slug == "terrenos-urbanos"

# This test verifies if the serializer handles Unicode characters properly
@pytest.mark.django_db
def test_serializer_handles_unicode_name():
    serializer = CategorySerializer(data={"name": "Terrenos & Propriedades"})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Terrenos & Propriedades"
    assert instance.slug == "terrenos-propriedades"

# This test verifies slug generation when special characters are present
@pytest.mark.django_db
def test_serializer_handles_special_characters():
    serializer = CategorySerializer(data={"name": "Terrenos @#$%^&*()"})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Terrenos @#$%^&*()"
    assert instance.slug == "terrenos"
