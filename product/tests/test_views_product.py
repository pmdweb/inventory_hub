import pytest
from rest_framework.test import APIClient

from catalog.models import Category
from product.models import Product

client = APIClient()


@pytest.mark.django_db
def test_list_products():
    category = Category.objects.create(name="Category A")
    Product.objects.create(name="Product 1", price=10.0, category=category)
    Product.objects.create(name="Product 2", price=20.0, category=category)

    response = client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.data) == 2
    names = [p["name"] for p in response.data]
    assert "Product 1" in names
    assert "Product 2" in names


@pytest.mark.django_db
def test_retrieve_product():
    category = Category.objects.create(name="Category A")
    product = Product.objects.create(name="Product 1", price=10.0, category=category)

    response = client.get(f"/api/products/{product.id}/")
    assert response.status_code == 200
    data = response.data
    assert data["id"] == product.id
    assert data["name"] == product.name
    assert float(data["price"]) == product.price


@pytest.mark.django_db
def test_create_product():
    category = Category.objects.create(name="Category A")

    payload = {
        "name": "New Product",
        "price": "15.99",
        "category": category.id,
    }

    response = client.post("/api/products/", data=payload, content_type="application/json")
    assert response.status_code == 201
    assert Product.objects.filter(name="New Product").exists()


@pytest.mark.django_db
def test_update_product():
    category = Category.objects.create(name="Category A")
    product = Product.objects.create(name="Old Name", price=10.0, category=category)

    payload = {
        "name": "Updated Name",
        "price": "12.50",
        "category": category.id,
    }

    response = client.put(
        f"/api/products/{product.id}/", data=payload, content_type="application/json"
    )
    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == "Updated Name"
    assert float(product.price) == 12.50


@pytest.mark.django_db
def test_delete_product():
    category = Category.objects.create(name="Category A")
    product = Product.objects.create(name="Product To Delete", price=10.0, category=category)

    response = client.delete(f"/api/products/{product.id}/")
    assert response.status_code == 204
    assert not Product.objects.filter(id=product.id).exists()
