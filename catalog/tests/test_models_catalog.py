import pytest
from catalog.models import Category

@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="RPG")
    assert str(category) == "RPG"

@pytest.mark.django_db
def test_slug_is_generated():
    category = Category.objects.create(name="Miniatura Legal")
    assert category.slug == "miniatura-legal"
