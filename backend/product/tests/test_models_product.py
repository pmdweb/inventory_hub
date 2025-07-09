import pytest

from catalog.models import Category
from product.models import Product


@pytest.mark.django_db
def test_product_str():
    """
    GIVEN a product with a name
    WHEN converted to string
    THEN it returns its name
    """
    category = Category.objects.create(name="Category A")
    product = Product.objects.create(
        name="Test Product",
        price=10.0,
        category=category,
        description="Some description",
    )

    assert str(product) == "Test Product"


@pytest.mark.django_db
def test_product_creation_with_all_fields():
    """
    GIVEN valid data for all fields
    WHEN creating a product
    THEN it is saved correctly
    """
    category = Category.objects.create(name="Category A")

    product = Product.objects.create(
        name="Complete Product",
        category=category,
        price=99.99,
        description="Full description",
        is_active=True,
    )

    assert product.id is not None
    assert product.name == "Complete Product"
    assert product.category == category
    assert float(product.price) == 99.99
    assert product.description == "Full description"
    assert product.is_active is True


@pytest.mark.django_db
def test_product_defaults():
    """
    GIVEN only required fields
    WHEN creating a product
    THEN optional fields assume their default values
    """
    category = Category.objects.create(name="Category A")

    product = Product.objects.create(
        name="Minimal Product", category=category, price=5.00
    )

    assert product.description in ("", None)
    assert product.is_active is True
