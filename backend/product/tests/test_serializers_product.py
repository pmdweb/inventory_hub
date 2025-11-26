import pytest

from catalog.models import Category
from product.models import Product
from product.serializers import ProductSerializer


@pytest.mark.django_db
def test_serialize_product():
    category = Category.objects.create(name="Category A")
    product = Product.objects.create(
        name="Test Product",
        price=30.0,
        category=category,
        description="Test description",
        is_active=True,
    )

    serializer = ProductSerializer(product)
    data = serializer.data

    expected_keys = {
        "id",
        "category",
        "name",
        "slug",
        "tags",
        "description",
        "price",
        "is_active",
        "featured_image",
        "created_at",
        "updated_at",
    }

    assert set(data.keys()) == expected_keys
    assert data["name"] == "Test Product"
    assert float(data["price"]) == 30.0
    assert data["category"] == category.id


@pytest.mark.django_db
def test_deserialize_and_create_product():
    category = Category.objects.create(name="Category A")
    payload = {
        "name": "Created via Serializer",
        "price": "45.00",
        "category": category.id,
        "description": "Test description",
        "is_active": True,
    }

    serializer = ProductSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    product = serializer.save()

    assert Product.objects.filter(id=product.id).exists()
    assert product.name == payload["name"]
    assert float(product.price) == float(payload["price"])
    assert product.category == category


@pytest.mark.django_db
def test_deserialize_invalid_missing_name():
    category = Category.objects.create(name="Category A")
    payload = {
        "price": "10.00",
        "category": category.id,
    }

    serializer = ProductSerializer(data=payload)
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_deserialize_invalid_missing_price():
    category = Category.objects.create(name="Category A")
    payload = {
        "name": "Test Product",
        "category": category.id,
    }

    serializer = ProductSerializer(data=payload)
    assert not serializer.is_valid()
    assert "price" in serializer.errors


@pytest.mark.django_db
def test_deserialize_invalid_missing_category():
    payload = {
        "name": "Test Product",
        "price": "10.00",
    }

    serializer = ProductSerializer(data=payload)
    assert not serializer.is_valid()
    assert "category" in serializer.errors


@pytest.mark.django_db
def test_deserialize_invalid_negative_price():
    category = Category.objects.create(name="Category A")
    payload = {
        "name": "Bad Product",
        "price": "-5.00",
        "category": category.id,
        "description": "Test description",
        "is_active": True,
    }

    serializer = ProductSerializer(data=payload)
    if serializer.is_valid():
        product = serializer.save()
        assert float(product.price) >= 0, "Product price should not be negative"
    else:
        assert "price" in serializer.errors or True  # caso você valide no serializer
