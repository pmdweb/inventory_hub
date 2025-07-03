import pytest
from catalog.models import Category
from catalog.serializers import CategorySerializer


@pytest.mark.django_db
def test_serializer_valid_data():
    data = {"name": "Terrenos"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Terrenos"
    assert instance.slug == "terrenos"


@pytest.mark.django_db
def test_serializer_rejects_empty_name():
    serializer = CategorySerializer(data={"name": ""})
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_serializer_rejects_duplicate_name():
    Category.objects.create(name="Terrenos")
    serializer = CategorySerializer(data={"name": "Terrenos"})
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_serializer_output_fields():
    category = Category.objects.create(name="Cenários")
    serializer = CategorySerializer(category)
    data = serializer.data
    assert data["name"] == "Cenários"
    assert data["slug"] == "cenarios"
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.django_db
def test_serializer_handles_unicode_name():
    serializer = CategorySerializer(data={"name": "Terrenos & Propriedades"})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Terrenos & Propriedades"
    # slugify transforma "&" em "e"
    assert instance.slug == "terrenos-propriedades"


@pytest.mark.django_db
def test_serializer_handles_special_characters():
    serializer = CategorySerializer(data={"name": "Terrenos @#$%^&*()"})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Terrenos @#$%^&*()"
    # slugify remove ou substitui caracteres especiais
    assert instance.slug.startswith("terrenos")


@pytest.mark.django_db
def test_serializer_rejects_too_long_name():
    long_name = "A" * 300  # exceeds 255
    serializer = CategorySerializer(data={"name": long_name})
    assert not serializer.is_valid()
    assert "name" in serializer.errors
    assert "ensure this field has no more than" in serializer.errors["name"][0].lower()


@pytest.mark.django_db
def test_read_only_fields_are_not_updated():
    """
    Ensure that read-only fields (slug, created_at, updated_at)
    cannot be updated through the serializer.
    """
    # Create initial Category instance
    category = Category.objects.create(name="Mapa")

    # Store the original read-only field values
    original_slug = category.slug
    original_created_at = category.created_at
    original_updated_at = category.updated_at

    # Attempt to update read-only fields
    data = {
        "name": "Mapa Atualizado",
        "slug": "forced-slug",
        "created_at": "2000-01-01T00:00:00Z",
        "updated_at": "2000-01-01T00:00:00Z",
    }

    serializer = CategorySerializer(category, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()

    # Validate that allowed field was updated
    assert instance.name == "Mapa Atualizado"

    # Validate that read-only fields remain unchanged
    assert instance.slug == original_slug
    assert instance.created_at == original_created_at
    assert instance.updated_at >= original_updated_at  # updated_at may auto-update
