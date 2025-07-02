import pytest
from rest_framework.test import APIClient
from catalog.models import Category

client = APIClient()

@pytest.mark.django_db
def test_list_categories():
    Category.objects.create(name="Criaturas")
    response = client.get("/api/categories/")
    assert response.status_code == 200
    assert response.data[0]["name"] == "Criaturas"
