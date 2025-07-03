import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from media_assets.models import MediaAsset


@pytest.mark.django_db
def test_mediaasset_str():
    file = SimpleUploadedFile(
        "test.pdf", b"file_content", content_type="application/pdf"
    )
    asset = MediaAsset.objects.create(name="Manual", file=file, license_type="cc-by")
    assert str(asset) == "Manual (cc-by)"


@pytest.mark.django_db
def test_slug_is_generated_only_on_create():
    file = SimpleUploadedFile("file.pdf", b"123", content_type="application/pdf")
    asset = MediaAsset.objects.create(
        name="Mapa Legal", file=file, license_type="cc-by"
    )
    slug_before = asset.slug

    # update name, slug should remain
    asset.name = "Mapa Muito Legal"
    asset.save()
    asset.refresh_from_db()

    assert asset.slug == slug_before


@pytest.mark.django_db
def test_optional_fields_are_saved():
    file = SimpleUploadedFile("file.pdf", b"123", content_type="application/pdf")
    asset = MediaAsset.objects.create(
        name="Mapa Completo",
        file=file,
        license_type="cc-by",
        tags="tag1,tag2",
        author="Pedro",
        license="Creative Commons",
        license_url="https://creativecommons.org",
        alt_text="Alt text here",
        description="Some description",
    )

    assert asset.tags == "tag1,tag2"
    assert asset.author == "Pedro"
    assert asset.license == "Creative Commons"
    assert asset.license_url == "https://creativecommons.org"
    assert asset.alt_text == "Alt text here"
    assert asset.description == "Some description"


@pytest.mark.django_db
def test_is_active_flag():
    file = SimpleUploadedFile("file.pdf", b"123", content_type="application/pdf")
    asset = MediaAsset.objects.create(
        name="Inactive Asset", file=file, license_type="cc-by", is_active=False
    )
    assert not asset.is_active
