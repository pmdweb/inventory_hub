import shutil
import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def cleanup_media_folder(tmp_path, settings):
    """Redirect MEDIA_ROOT to a temp folder and clean up after tests."""
    settings.MEDIA_ROOT = tmp_path
    yield
    shutil.rmtree(tmp_path, ignore_errors=True)
