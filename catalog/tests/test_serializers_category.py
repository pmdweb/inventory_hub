import pytest
from catalog.serializers import CategorySerializer

@pytest.mark.django_db
def test_category_serializer_create():
    data = {"name": "Terrenos"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.slug == "terrenos"
    assert instance.name == "Terrenos"
    