import pytest
from src.betteredit.config import Settings

@pytest.fixture(scope="session")
def cfg():
    # Load settings using Settings.load() which handles path resolution correctly
    return Settings.load()