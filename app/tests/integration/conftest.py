import os
from fakeredis import FakeRedis
import pytest
from fastapi.testclient import TestClient
from app import app  # Импортируем ваше FastAPI приложение
from settings import TestState


@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def test_client():
    os.environ["is_testing"] = TestState.TRUE
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    os.environ["is_testing"] = TestState.FALSE
