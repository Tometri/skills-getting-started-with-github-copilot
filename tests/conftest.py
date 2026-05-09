import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

@pytest.fixture
def client(monkeypatch):
    """Provide a TestClient with a fresh copy of the in-memory activities store for each test."""
    fresh = copy.deepcopy(app_module.activities)
    monkeypatch.setattr(app_module, "activities", fresh)
    return TestClient(app_module.app)
