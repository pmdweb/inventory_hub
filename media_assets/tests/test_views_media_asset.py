import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from media_assets.models import MediaAsset

client = APIClient()

@pytest.mark.django_db
def test_list_media_assets():
    MediaAsset.objects.create(
        name="Dungeon Map",
        file=SimpleUploadedFile("map.pdf", b"fake content"),
        license_type="free",
    )
    response = client.get("/api/media-assets/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Dungeon Map"

@pytest.mark.django_db
def test_create_media_asset():
    file = SimpleUploadedFile("book.pdf", b"123", content_type="application/pdf")
    data = {
        "name": "RPG Book",
        "file": file,
        "license_type": "cc-by-sa"
    }
    response = client.post("/api/media-assets/", data, format="multipart")
    assert response.status_code == 201
    assert response.data["name"] == "RPG Book"
    assert response.data["license_type"] == "cc-by-sa"
    assert "file" in response.data
    assert "media_library/" in response.data["file"]

@pytest.mark.django_db
def test_get_single_media_asset():
    asset = MediaAsset.objects.create(
        name="Hero Token",
        file=SimpleUploadedFile("token.pdf", b"abc"),
        license_type="cc-by"
    )
    response = client.get(f"/api/media-assets/{asset.id}/")
    assert response.status_code == 200
    assert response.data["name"] == "Hero Token"

@pytest.mark.django_db
def test_patch_media_asset():
    asset = MediaAsset.objects.create(
        name="Old Token",
        file=SimpleUploadedFile("token.pdf", b"abc"),
        license_type="free"
    )
    data = {"name": "Updated Token"}
    response = client.patch(f"/api/media-assets/{asset.id}/", data, format="json")
    assert response.status_code == 200
    assert response.data["name"] == "Updated Token"

@pytest.mark.django_db
def test_delete_media_asset():
    asset = MediaAsset.objects.create(
        name="To Delete",
        file=SimpleUploadedFile("delete.pdf", b"delete me"),
        license_type="free"
    )
    response = client.delete(f"/api/media-assets/{asset.id}/")
    assert response.status_code == 204
    assert MediaAsset.objects.count() == 0
