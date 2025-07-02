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
