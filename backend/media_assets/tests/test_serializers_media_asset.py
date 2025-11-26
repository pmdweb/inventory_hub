import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from media_assets.models import MediaAsset
from media_assets.serializers import MediaAssetSerializer


@pytest.mark.django_db
def test_serializer_outputs_expected_fields():
    fake_file = SimpleUploadedFile(
        "mapa.pdf", b"conteudo", content_type="application/pdf"
    )
    asset = MediaAsset.objects.create(
        name="Mapa de RPG", file=fake_file, license_type="cc-by"
    )
    serializer = MediaAssetSerializer(asset)
    data = serializer.data

    assert data["name"] == "Mapa de RPG"
    assert data["license_type"] == "cc-by"
    assert data["file"] is not None
    assert "media_library/" in data["file"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "upload_at" in data


@pytest.mark.django_db
def test_serializer_rejects_missing_file():
    serializer = MediaAssetSerializer(
        data={"name": "Sem Arquivo", "license_type": "cc-by"}
    )
    assert not serializer.is_valid()
    assert "file" in serializer.errors
    assert "no file was submitted" in serializer.errors["file"][0].lower()


@pytest.mark.django_db
def test_serializer_rejects_invalid_license_type():
    file = SimpleUploadedFile("manual.pdf", b"data", content_type="application/pdf")
    serializer = MediaAssetSerializer(
        data={
            "name": "Licença Inválida",
            "file": file,
            "license_type": "invalid-license",
        }
    )
    assert not serializer.is_valid()
    assert "license_type" in serializer.errors
    assert "valid choice" in serializer.errors["license_type"][0].lower()


@pytest.mark.django_db
def test_read_only_fields_cannot_be_updated():
    fake_file = SimpleUploadedFile(
        "manual.pdf", b"file_content", content_type="application/pdf"
    )
    asset = MediaAsset.objects.create(
        name="Asset Original", file=fake_file, license_type="cc-by"
    )

    original_created = asset.created_at
    original_updated = asset.updated_at
    original_slug = asset.slug

    data = {
        "created_at": "2000-01-01T00:00:00Z",
        "updated_at": "2000-01-01T00:00:00Z",
        "slug": "forcado",
        "name": "Asset Atualizado",
    }

    serializer = MediaAssetSerializer(asset, data=data, partial=True)
    assert serializer.is_valid()
    instance = serializer.save()

    assert instance.created_at == original_created
    assert instance.updated_at >= original_updated  # updated_at will auto-update
    assert instance.slug == original_slug
    assert instance.name == "Asset Atualizado"


@pytest.mark.django_db
def test_serializer_accepts_special_characters_in_name():
    file = SimpleUploadedFile("manual.pdf", b"data", content_type="application/pdf")
    serializer = MediaAssetSerializer(
        data={"name": "Nome com !@#$$%", "file": file, "license_type": "cc-by"}
    )
    assert serializer.is_valid()
