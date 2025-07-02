import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from media_assets.models import MediaAsset
from media_assets.serializers import MediaAssetSerializer


@pytest.mark.django_db
def test_media_asset_serializer_output_fields():
    """Ensure serialized fields are present and correctly rendered."""
    fake_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    asset = MediaAsset.objects.create(name="Manual de RPG", file=fake_file, license_type="free")

    serializer = MediaAssetSerializer(asset)
    data = serializer.data

    assert data["name"] == "Manual de RPG"
    assert data["license_type"] == "free"
    assert data["file"] is not None
    assert "media_assets/" in data["file"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.django_db
def test_media_asset_serializer_creates_instance():
    """Ensure a valid serializer input creates a new MediaAsset."""
    fake_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    payload = {
        "name": "Mapa de Dungeon",
        "license_type": "paid",
        "file": fake_file,
    }

    serializer = MediaAssetSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    instance = serializer.save()
    assert instance.name == "Mapa de Dungeon"
    assert instance.license_type == "paid"
    assert instance.file.name.startswith("media_assets/")


@pytest.mark.django_db
def test_serializer_rejects_missing_file():
    """Should raise validation error if file is missing."""
    payload = {"name": "Sem Arquivo", "license_type": "free"}
    serializer = MediaAssetSerializer(data=payload)

    assert not serializer.is_valid()
    assert "file" in serializer.errors
    assert "This field is required." in str(serializer.errors["file"])


@pytest.mark.django_db
def test_serializer_rejects_invalid_license():
    """Should raise error for invalid license_type value."""
    fake_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    payload = {"name": "Licença Inválida", "license_type": "open", "file": fake_file}

    serializer = MediaAssetSerializer(data=payload)
    assert not serializer.is_valid()
    assert "license_type" in serializer.errors
    assert "is not a valid choice" in str(serializer.errors["license_type"])


@pytest.mark.django_db
def test_serializer_rejects_blank_name():
    """Should not allow empty name field."""
    fake_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    payload = {"name": "", "license_type": "free", "file": fake_file}

    serializer = MediaAssetSerializer(data=payload)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
    assert "may not be blank" in str(serializer.errors["name"])


@pytest.mark.django_db
def test_serializer_blocks_readonly_fields_on_input():
    """Should not allow setting read-only fields manually."""
    fake_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    asset = MediaAsset.objects.create(name="Mapa 2", file=fake_file, license_type="free")

    payload = {
        "name": "Mapa Atualizado",
        "created_at": "2022-01-01T00:00:00Z",
        "updated_at": "2022-01-01T00:00:00Z",
    }

    serializer = MediaAssetSerializer(asset, data=payload, partial=True)
    assert not serializer.is_valid()
    assert "created_at" in serializer.errors
    assert "updated_at" in serializer.errors


@pytest.mark.django_db
def test_serializer_allows_special_characters_in_name():
    """Should allow special characters in name field."""
    fake_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    payload = {"name": "Manual @#$%", "license_type": "free", "file": fake_file}

    serializer = MediaAssetSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Manual @#$%"


@pytest.mark.django_db
def test_media_asset_str_representation():
    """Ensure string representation matches expected format."""
    fake_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    asset = MediaAsset.objects.create(name="Cartaz", file=fake_file, license_type="free")

    assert str(asset) == "Cartaz (free)"
