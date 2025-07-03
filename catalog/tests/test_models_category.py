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


@pytest.mark.django_db
def test_category_ordering():
    Category.objects.create(name="B")
    Category.objects.create(name="A")
    categories = Category.objects.all()
    names = [c.name for c in categories]
    assert names == sorted(names)
