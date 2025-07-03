import pytest
from media_assets.models import MediaAsset
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_mediaasset_creation():
    fake_file = SimpleUploadedFile("test.pdf", b"file_content")
    asset = MediaAsset.objects.create(
        name="Manual de RPG",
        file=fake_file,
        license_type="free"
    )
    assert asset.name == "Manual de RPG"
    assert asset.license_type == "free"
    assert asset.file.name.startswith("media_library/")

@pytest.mark.django_db
def test_media_asset_str_representation():
    fake_file = SimpleUploadedFile("manual.pdf", b"content", content_type="application/pdf")
    asset = MediaAsset.objects.create(
        name="Livro de Regras",
        file=fake_file,
        license_type="cc-by-sa"
    )
    assert str(asset) == "Livro de Regras (cc-by-sa)"

@pytest.mark.django_db
def test_media_asset_fields_persist():
    fake_file = SimpleUploadedFile("manual.pdf", b"content", content_type="application/pdf")
    asset = MediaAsset.objects.create(
        name="Mapa de Dungeon",
        file=fake_file,
        license_type="cc0",
        tags="rpg,mapa",
        author="Pedro",
        license="Creative Commons",
        license_url="https://creativecommons.org/publicdomain/zero/1.0/",
        alt_text="Um mapa antigo",
        description="Mapa detalhado de uma masmorra"
    )

    assert asset.name == "Mapa de Dungeon"
    assert asset.license_type == "cc0"
    assert asset.author == "Pedro"
    assert asset.file.name.startswith("media_library/")
