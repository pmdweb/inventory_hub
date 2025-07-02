import pytest
from rest_framework.test import APIClient
from catalog.models import Category

client = APIClient()

# Test the GET request to list categories
@pytest.mark.django_db
def test_list_categories():
    Category.objects.create(name="Criaturas")
    response = client.get("/api/categories/")
    assert response.status_code == 200
    assert response.data[0]["name"] == "Criaturas"

# Test the POST request to create a valid category
@pytest.mark.django_db
def test_create_category():
    data = {"name": "Terrenos"}
    response = client.post("/api/categories/", data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Terrenos"
    assert response.data["slug"] == "terrenos"

# Test the POST request with empty name (invalid)
@pytest.mark.django_db
def test_create_category_invalid_name():
    data = {"name": ""}
    response = client.post("/api/categories/", data, format="json")
    assert response.status_code == 400
    assert "name" in response.data

# Test the POST request with duplicate name (should fail)
@pytest.mark.django_db
def test_create_category_duplicate_name():
    Category.objects.create(name="Terrenos")
    data = {"name": "Terrenos"}
    response = client.post("/api/categories/", data, format="json")
    assert response.status_code == 400
    assert "name" in response.data

# # Test the POST request with invalid characters in name
# @pytest.mark.django_db
# def test_create_category_invalid_characters():
#     data = {"name": "123"}
#     response = client.post("/api/categories/", data, format="json")
#     assert response.status_code == 400
#     assert "name" in response.data

# Test the POST request with a valid complex name
@pytest.mark.django_db
def test_create_category_valid_name():
    data = {"name": "Terrenos Urbanos"}
    response = client.post("/api/categories/", data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Terrenos Urbanos"
    assert response.data["slug"] == "terrenos-urbanos"

# Test retrieving a single category by ID
@pytest.mark.django_db
def test_get_category_by_id():
    category = Category.objects.create(name="Armas")
    response = client.get(f"/api/categories/{category.id}/")
    assert response.status_code == 200
    assert response.data["name"] == "Armas"
    assert response.data["slug"] == "armas"

# Test full update (PUT) of a category
@pytest.mark.django_db
def test_put_category():
    category = Category.objects.create(name="Cenários")
    data = {"name": "Cenários Atualizados"}
    response = client.put(f"/api/categories/{category.id}/", data, format="json")
    assert response.status_code == 200
    assert response.data["name"] == "Cenários Atualizados"
    assert response.data["slug"] == "cenarios-atualizados"

# Test partial update (PATCH) of a category
@pytest.mark.django_db
def test_patch_category():
    category = Category.objects.create(name="Tokens")
    data = {"name": "Tokens de Combate"}
    response = client.patch(f"/api/categories/{category.id}/", data, format="json")
    assert response.status_code == 200
    assert response.data["name"] == "Tokens de Combate"
    assert response.data["slug"] == "tokens-de-combate"

# Test deleting a category
@pytest.mark.django_db
def test_delete_category():
    category = Category.objects.create(name="Itens Mágicos")
    response = client.delete(f"/api/categories/{category.id}/")
    assert response.status_code == 204

    # Confirm it no longer exists
    get_response = client.get(f"/api/categories/{category.id}/")
    assert get_response.status_code == 404
