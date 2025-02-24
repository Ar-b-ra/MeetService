from fakeredis import FakeStrictRedis
import pytest
from fastapi.testclient import TestClient
from app import app  # Импортируем ваше FastAPI приложение
from settings import TestState
from settings import REDIS_SETTINGS


@pytest.fixture
def fake_redis():
    return FakeStrictRedis(
        host=REDIS_SETTINGS.redis_host,
        port=REDIS_SETTINGS.redis_port,
        db=REDIS_SETTINGS.redis_db,
    )


@pytest.fixture
def test_client():
    REDIS_SETTINGS.is_testing = TestState.TRUE
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    REDIS_SETTINGS.is_testing = TestState.FALSE
