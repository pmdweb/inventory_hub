import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from media_assets.models import MediaAsset

client = APIClient()


@pytest.mark.django_db
def test_list_media_assets():
    MediaAsset.objects.create(
        name="Mapa",
        file=SimpleUploadedFile("mapa.pdf", b"fake content"),
        license_type="free",
    )

    response = client.get("/api/media-assets/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Mapa"


@pytest.mark.django_db
def test_create_media_asset():
    file = SimpleUploadedFile("file.pdf", b"123", content_type="application/pdf")
    data = {
        "name": "Novo Arquivo",
        "file": file,
        "license_type": "paid"
    }

    response = client.post("/api/media-assets/", data, format="multipart")
    assert response.status_code == 201
    assert response.data["name"] == "Novo Arquivo"
    assert response.data["license_type"] == "paid"
    assert "file" in response.data
    assert "media_assets/" in response.data["file"]


@pytest.mark.django_db
def test_get_single_media_asset():
    asset = MediaAsset.objects.create(
        name="Token",
        file=SimpleUploadedFile("token.pdf", b"abc"),
        license_type="free"
    )

    response = client.get(f"/api/media-assets/{asset.id}/")
    assert response.status_code == 200
    assert response.data["name"] == "Token"


@pytest.mark.django_db
def test_patch_media_asset():
    asset = MediaAsset.objects.create(
        name="Token Antigo",
        file=SimpleUploadedFile("token.pdf", b"abc"),
        license_type="free"
    )

    data = {"name": "Token Atualizado"}
    response = client.patch(f"/api/media-assets/{asset.id}/", data, format="json")
    assert response.status_code == 200
    assert response.data["name"] == "Token Atualizado"


@pytest.mark.django_db
def test_delete_media_asset():
    asset = MediaAsset.objects.create(
        name="Pra Deletar",
        file=SimpleUploadedFile("delete.pdf", b"delete me"),
        license_type="free"
    )

    response = client.delete(f"/api/media-assets/{asset.id}/")
    assert response.status_code == 204
    assert MediaAsset.objects.count() == 0
