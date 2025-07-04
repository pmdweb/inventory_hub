import shutil

import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def cleanup_media_folder(tmp_path, settings):
    """
    Redirect MEDIA_ROOT to a temporary path during tests.
    Ensures no leftover files affect the next run.
    """
    settings.MEDIA_ROOT = tmp_path
    settings.MEDIA_URL = "/media/"  # Ensures serializer URLs remain consistent
    yield
    shutil.rmtree(tmp_path, ignore_errors=True)
